from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.cache import get_cached_doctors, cache_doctors_list, invalidate_doctors_cache
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
    NurseCreate, NurseResponse,
    StaffCreate, StaffResponse,
    SpecialtyCreate, SpecialtyResponse,
    EmployeeResponse
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
        consultation_fee=payload.consultation_fee
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    
    invalidate_doctors_cache()

    return doctor

# -------------------------------
# Update Doctor
# -------------------------------
def update_doctor(doctor_id: UUID, payload: DoctorUpdate, db: Session):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if payload.specialty:
        doctor.specialty = payload.specialty
    if payload.consultation_fee:
        doctor.consultation_fee = payload.consultation_fee

    db.commit()
    db.refresh(doctor)
    
    invalidate_doctors_cache()

    return doctor

# -------------------------------
# Add Nurse
# -------------------------------
def add_nurse(payload: NurseCreate, db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- ASSIGN ROLE: nurse ---
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
    return nurse


# -------------------------------
# Add Staff
# -------------------------------
def add_staff(payload: StaffCreate, db: Session):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --- ASSIGN ROLE: staff ---
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
    return staff


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

    cached_doctors = get_cached_doctors()
    if cached_doctors:
        return cached_doctors
    
    users = db.query(User).all()
    employees = []

    for user in users:
        employees.append(EmployeeResponse(
            id=user.id,
            email=user.email,
            roles=[r.name for r in user.roles],
            doctor_profile=(
                DoctorResponse.model_validate(user.doctor_profile, from_attributes=True)
                if user.doctor_profile else None
            ),
            nurse_profile=(
                NurseResponse.model_validate(user.nurse_profile, from_attributes=True)
                if user.nurse_profile else None
            ),
            staff_profile=(
                StaffResponse.model_validate(user.staff_profile, from_attributes=True)
                if user.staff_profile else None
            ),
        ))

    cache_doctors_list(employees)

    return employees
