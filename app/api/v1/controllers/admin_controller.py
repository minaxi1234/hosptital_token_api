from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.cache import  invalidate_doctors_cache
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import user_roles_table
from app.models.doctor import Doctor
from app.models.nurse import Nurse
from app.models.staff import Staff
from app.models.specialty import Specialty

from app.api.v1.schemas.admin import (
    DoctorCreate, DoctorUpdate, DoctorResponse,
    NurseCreate, NurseResponse, NurseUpdate,
    StaffCreate, StaffResponse,
    SpecialtyCreate, SpecialtyResponse,
    EmployeeResponse, StaffUpdate
)

# -------------------------------
# Add Doctor
# -------------------------------
def add_doctor(payload: DoctorCreate, db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- ASSIGN ROLE: doctor ---
    doctor_role = db.query(Role).filter(Role.name == "doctor").first()
    if doctor_role and doctor_role not in user.roles:
        user.roles.append(doctor_role)

    doctor = Doctor(
        user_id=payload.user_id,
        specialty=payload.specialty,
        consultation_fee=payload.consultation_fee,
        
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    
    invalidate_doctors_cache()

    return DoctorResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialty=doctor.specialty,
        consultation_fee=doctor.consultation_fee,
        email=user.email,
    )

# -------------------------------
# Update Doctor
# -------------------------------
def update_doctor(doctor_id: UUID, payload: DoctorUpdate, db: Session):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if payload.specialty:
        doctor.specialty = payload.specialty
    if payload.consultation_fee is not None:
        doctor.consultation_fee = payload.consultation_fee

    db.commit()
    db.refresh(doctor)

    user = db.query(User).filter(User.id == doctor.user_id).first()

    return DoctorResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialty=doctor.specialty,
        consultation_fee=doctor.consultation_fee,
        email=user.email,
    )


def get_all_doctors(db: Session):
    results = (
        db.query(Doctor, User.email)
        .join(User, Doctor.user_id == User.id)
        .all()
    )

    return [
        DoctorResponse(
            id=doctor.id,
            user_id=doctor.user_id,
            specialty=doctor.specialty,
            consultation_fee=doctor.consultation_fee,
            email=email,
        )
        for doctor, email in results
    ]


# -------------------------------
# Add Nurse
# -------------------------------
def add_nurse(payload: NurseCreate, db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    nurse_role = db.query(Role).filter(Role.name == "nurse").first()
    if nurse_role and nurse_role not in user.roles:
        user.roles.append(nurse_role)

    nurse = Nurse(
        user_id=payload.user_id,
        department=payload.department
    )

    db.add(nurse)
    db.commit()
    db.refresh(nurse)

    return NurseResponse(
        id=nurse.id,
        user_id=nurse.user_id,
        department=nurse.department,
        email=user.email,
    )


def update_nurse(nurse_id: UUID, payload: NurseUpdate, db: Session):
    nurse = db.query(Nurse).filter(Nurse.id == nurse_id).first()
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")

    nurse.department = payload.department
    db.commit()
    db.refresh(nurse)

    user = db.query(User).filter(User.id == nurse.user_id).first()
    if not user:
        raise HTTPException(status_code=500, detail="Linked user not found")

    return NurseResponse(
        id=nurse.id,
        user_id=nurse.user_id,
        department=nurse.department,
        email=user.email,
    )



# -------------------------------
# Add Staff
# -------------------------------
def add_staff(payload: StaffCreate, db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    staff_role = db.query(Role).filter(Role.name == "staff").first()
    if staff_role and staff_role not in user.roles:
        user.roles.append(staff_role)

    staff = Staff(
        user_id=payload.user_id,
        department=payload.department
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return StaffResponse(
        id=staff.id,
        user_id=staff.user_id,
        department=staff.department,
        email=user.email,
    )


def update_staff(staff_id: UUID, payload: StaffUpdate, db: Session):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    staff.department = payload.department
    db.commit()
    db.refresh(staff)

    user = db.query(User).filter(User.id == staff.user_id).first()

    return StaffResponse(
        id=staff.id,
        user_id=staff.user_id,
        department=staff.department,
        email=user.email,
    )


# -------------------------------
# Add Specialty
# -------------------------------
def add_specialty(payload: SpecialtyCreate, db: Session):
    existing = db.query(Specialty).filter(Specialty.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Specialty already exists")
    
    specialty = Specialty(name=payload.name)
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty

# -------------------------------
# View All Employees
# -------------------------------
def view_all_employees(db: Session):
    users = db.query(User).all()
    employees = []

    for user in users:
        employees.append(EmployeeResponse(
            id=user.id,
            email=user.email,
            roles=[r.name for r in user.roles],
            doctor_profile=None,
            nurse_profile=None,
            staff_profile=None,
        ))

    return employees
