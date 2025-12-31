from datetime import datetime, time
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.user import User
from app.api.v1.schemas.admin import DoctorResponse

from datetime import date
from app.db.session import get_db
from app.models.patient import Patient
from app.models.token import Token, TokenStatus
from app.models.doctor import Doctor
from app.api.v1.schemas.patient_token import PatientCreate, PatientRead, TokenCreate, TokenRead, TokenUpdateStatus
from app.models.user import User
from app.core.rbac import require_roles # our RBAC decorator
from app.core.websocket_manager import websocket_manager
import asyncio

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/", response_model=list[PatientRead])
def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["staff", "admin"]))
):
    return db.query(Patient).all()

# -------------------------------
# 1️⃣ Patient Registration
# -------------------------------
@router.post("/", response_model=PatientRead)
  # Only staff/admin can register patients
def register_patient(patient_in: PatientCreate, db: Session = Depends(get_db), current_user = Depends(require_roles(["staff", "admin"]))):
    existing = db.query(Patient).filter(
        (Patient.email == patient_in.email) | (Patient.phone == patient_in.phone)
    ).first()
    if existing:
        raise HTTPException(400, "Patient already exists")
    patient = Patient(
        name=patient_in.name,
        email=patient_in.email,
        phone=patient_in.phone,
        age=patient_in.age
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)


    return patient

# -------------------------------
# 2️⃣ Generate Token
# -------------------------------
@router.post("/token", response_model=TokenRead)
# Only staff/admin can issue tokens
async def create_token(data: TokenCreate, db: Session = Depends(get_db), current_user = Depends(require_roles(["staff", "admin"]))):
    # Check doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check patient exists
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Generate next token number for this doctor
    today = datetime.utcnow().date()
    last_token = db.query(Token).filter(Token.doctor_id == doctor.id, Token.created_at >= today).order_by(Token.created_at.desc()).first()
    next_number = 1
    if last_token:
        try:
            next_number = int(last_token.token_number) + 1
        except ValueError:
            next_number = 1  # fallback if token_number is not numeric

    token = Token(
        token_number=str(next_number),
        patient_id=patient.id,
        doctor_id=doctor.id,
        status=TokenStatus.waiting
    )
    db.add(token)
    db.commit()
    db.refresh(token)

   
    await websocket_manager.broadcast({
        "event": "TOKEN_CREATED",
        "token_id": str(token.id),
        "token_number": token.token_number,
        "doctor_id": str(token.doctor_id),
        "patient_id": str(token.patient_id),
        "patient_name": patient.name,
        "status": token.status.value,
    })

    
   
    
    
    
    return token

# -------------------------------
# 3️⃣ Doctor Dashboard - View Own Tokens
# -------------------------------
@router.get("/tokens", response_model=list[TokenRead])

def doctor_tokens(current_user: User = Depends(require_roles(["doctor"])), db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    tokens = db.query(Token).filter(Token.doctor_id == doctor.id).order_by(Token.created_at.asc()).all()
    return tokens

# -------------------------------
# 4️⃣ Doctor Updates Token Status
# -------------------------------
@router.patch("/tokens/{token_id}", response_model=TokenRead)
async def update_token_status(
    token_id: uuid.UUID,
    update: TokenUpdateStatus,
    current_user: User = Depends(require_roles(["doctor"])),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    token = db.query(Token).filter(
        Token.id == token_id,
        Token.doctor_id == doctor.id
    ).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.status = update.status
    db.commit()
    db.refresh(token)

    # ✅ SAFE WebSocket broadcast (NO 500 possible)
    await websocket_manager.broadcast({
        "event": "TOKEN_STATUS_UPDATED",
        "token_id": str(token.id),
        "status": token.status.value,
        "doctor_id": str(token.doctor_id),
    })

    return token







@router.get("/tokens/today", response_model=list[TokenRead])
def staff_today_tokens(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["staff", "admin"]))
):
    start_of_day = datetime.combine(date.today(), time.min)

    tokens = (
        db.query(Token)
        .filter(Token.created_at >= start_of_day)
        .order_by(Token.created_at.asc())
        .all()
    )

    return tokens




@router.get("/doctors", response_model=list[DoctorResponse])
def staff_list_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["staff", "admin"]))
):
    results = (
        db.query(Doctor, User.email)
        .join(User, Doctor.user_id == User.id)
        .all()
    )

    return [
        DoctorResponse(
            id=d.id,
            user_id=d.user_id,
            specialty=d.specialty,
            consultation_fee=d.consultation_fee,
            email=email,
        )
        for d, email in results
    ]

@router.get("/tokens/public/today", response_model=list[TokenRead])
def public_today_tokens(db: Session = Depends(get_db)):
    start_of_day = datetime.combine(date.today(), time.min)

    tokens = (
        db.query(Token)
        .filter(
            Token.created_at >= start_of_day,
            Token.status != TokenStatus.completed
        )
        .order_by(Token.created_at.asc())
        .all()
    )

    return tokens
