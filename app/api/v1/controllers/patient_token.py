import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


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

# -------------------------------
# 1️⃣ Patient Registration
# -------------------------------
@router.post("/", response_model=PatientRead)
  # Only staff/admin can register patients
def register_patient(patient_in: PatientCreate, db: Session = Depends(get_db), current_user = Depends(require_roles(["staff", "admin"]))):
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
    last_token = db.query(Token).filter(Token.doctor_id == doctor.id).order_by(Token.created_at.desc()).first()
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

   
   

    message = {
        "type": "new_token",
        "token_id": str(token.id),
        "token_number": token.token_number,
        "doctor_id": str(token.doctor_id),
        "patient_name": patient.name,
        "status": token.status
    }
    print(f"🔄 DEBUG: Message to broadcast: {message}")
    print(f"🔄 DEBUG: Active connections: {len(websocket_manager.active_connections)}")
    
    try:
        await websocket_manager.broadcast_message(message)
        print("✅ DEBUG: WebSocket broadcast successful!")
    except Exception as e:
        print(f"❌ DEBUG: WebSocket error: {e}")
    
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
def update_token_status(token_id: uuid.UUID, update: TokenUpdateStatus,current_user: User = Depends(require_roles(["doctor"])), db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    token = db.query(Token).filter(Token.id == token_id, Token.doctor_id == doctor.id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.status = update.status
    db.commit()
    db.refresh(token)
    return token
