from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID


from app.db.session import get_db
from app.api.v1.controllers.admin_controller import (
    add_doctor, update_doctor,
    add_nurse, add_staff,
    add_specialty, view_all_employees
)
from app.api.v1.schemas.admin import (
    DoctorCreate, DoctorUpdate, DoctorResponse,
    NurseCreate, NurseResponse,
    StaffCreate, StaffResponse,
    SpecialtyCreate, SpecialtyResponse,
    EmployeeResponse
)

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

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    db.delete(doctor)
    db.commit()

    return {"message": "Doctor deleted successfully"}


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


@router.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))):
    return view_all_employees(db)
