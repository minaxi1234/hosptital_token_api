from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.cache import invalidate_doctors_cache
from app.db.session import get_db
from app.api.v1.controllers.admin_controller import (
    add_doctor, get_all_doctors, update_doctor,
    add_nurse, add_staff,
    add_specialty, update_nurse, update_staff, view_all_employees
)
from app.api.v1.schemas.admin import (
    DoctorCreate, DoctorUpdate, DoctorResponse,
    NurseCreate, NurseResponse, NurseUpdate,
    StaffCreate, StaffResponse,
    SpecialtyCreate, SpecialtyResponse,
    EmployeeResponse, StaffUpdate
)

from app.models.doctor import Doctor
from app.models.nurse import Nurse
from app.models.specialty import Specialty
from app.models.staff import Staff
from app.models.user import User

from app.core.rbac import require_roles  # our RBAC dependency

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# -------------------------------
# Admin-only endpoints
# -------------------------------

@router.post("/doctor", response_model=DoctorResponse)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db),current_user: User = Depends(require_roles(["admin"]))):
    return add_doctor(payload, db)


@router.put("/doctor/{doctor_id}", response_model=DoctorResponse)
def edit_doctor(doctor_id: UUID, payload: DoctorUpdate, db: Session = Depends(get_db),
current_user: User = Depends(require_roles(["admin"]))):
    return update_doctor(doctor_id, payload, db)


@router.delete("/doctor/{doctor_id}", status_code=200)
def delete_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    from app.models.doctor import Doctor
    from app.models.token import Token  # IMPORT ONLY THIS

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # 🔒 CRITICAL SAFETY CHECK
    token_exists = db.query(Token).filter(Token.doctor_id == doctor_id).first()
    if token_exists:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete doctor with existing tokens"
        )

    db.delete(doctor)
    db.commit()

    

    return {"message": "Doctor deleted successfully"}

@router.get("/doctors", response_model=List[DoctorResponse])
def list_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    return get_all_doctors(db)

@router.get("/doctor/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    user = db.query(User).filter(User.id == doctor.user_id).first()

    return DoctorResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialty=doctor.specialty,
        consultation_fee=doctor.consultation_fee,
        email=user.email,
    )



@router.post("/nurse", response_model=NurseResponse)
def create_nurse(payload: NurseCreate, db: Session = Depends(get_db),
current_user: User = Depends(require_roles(["admin"]))):
    return add_nurse(payload, db)

@router.delete("/nurse/{nurse_id}", status_code=200)
def delete_nurse(
    nurse_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    from app.models.nurse import Nurse

    nurse = db.query(Nurse).filter(Nurse.id == nurse_id).first()
    if not nurse:
        raise HTTPException(404, "Nurse not found")

    db.delete(nurse)
    db.commit()

    return {"message": "Nurse deleted successfully"}

@router.get("/nurses", response_model=List[NurseResponse])
def list_nurses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    results = (
        db.query(Nurse, User.email)
        .join(User, Nurse.user_id == User.id)
        .all()
    )

    return [
        NurseResponse(
            id=n.id,
            user_id=n.user_id,
            department=n.department,
            email=email,
        )
        for n, email in results
    ]


@router.put("/nurse/{nurse_id}", response_model=NurseResponse)
def edit_nurse(
    nurse_id: UUID,
    payload: NurseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    return update_nurse(nurse_id, payload, db)


@router.post("/staff", response_model=StaffResponse)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db),
current_user: User = Depends(require_roles(["admin"]))):
    return add_staff(payload, db)

@router.delete("/staff/{staff_id}", status_code=200)
def delete_staff(
    staff_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    from app.models.staff import Staff

    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(404, "Staff not found")

    db.delete(staff)
    db.commit()

    return {"message": "Staff deleted successfully"}

@router.get("/staff", response_model=List[StaffResponse])
def list_staff(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    results = (
        db.query(Staff, User.email)
        .join(User, Staff.user_id == User.id)
        .all()
    )

    return [
        StaffResponse(
            id=s.id,
            user_id=s.user_id,
            department=s.department,
            email=email,
        )
        for s, email in results
    ]


@router.put("/staff/{staff_id}", response_model=StaffResponse)
def edit_staff(
    staff_id: UUID,
    payload: StaffUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    return update_staff(staff_id, payload, db)



@router.post("/specialty", response_model=SpecialtyResponse)
def create_specialty(payload: SpecialtyCreate, db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))):
    return add_specialty(payload, db)

@router.delete("/specialty/{specialty_id}", status_code=200)
def delete_specialty(
    specialty_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    from app.models.specialty import Specialty

    specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not specialty:
        raise HTTPException(404, "Specialty not found")

    db.delete(specialty)
    db.commit()

    return {"message": "Specialty deleted successfully"}

@router.get("/specialties", response_model=List[SpecialtyResponse])
def list_specialties(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    return db.query(Specialty).all()


@router.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))):
    return view_all_employees(db)
