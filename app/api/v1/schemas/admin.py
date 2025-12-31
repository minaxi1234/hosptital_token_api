from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID

# -------------------------------
# Doctor Schemas
# -------------------------------
class DoctorCreate(BaseModel):
    user_id: UUID
    specialty: str = Field(..., max_length=100)
    consultation_fee: float = Field(..., gt=0)

class DoctorUpdate(BaseModel):
    specialty: Optional[str] = Field(None, max_length=100)
    consultation_fee: Optional[float] = Field(None, gt=0)

class DoctorResponse(BaseModel):
    id: UUID
    user_id: UUID
    specialty: str
    consultation_fee: float
    email: str

    class Config:
        orm_mode = True

# -------------------------------
# Nurse Schemas
# -------------------------------
class NurseCreate(BaseModel):
    user_id: UUID
    department: Optional[str] = Field(None, max_length=100)

class NurseResponse(BaseModel):
    id: UUID
    user_id: UUID
    department: Optional[str]
    email: str

    class Config:
        orm_mode = True

# -------------------------------
# Staff Schemas
# -------------------------------
class StaffCreate(BaseModel):
    user_id: UUID
    department: Optional[str] = Field(None, max_length=100)

class StaffResponse(BaseModel):
    id: UUID
    user_id: UUID
    department: Optional[str]
    email: str

    class Config:
        orm_mode = True

# -------------------------------
# Specialty Schemas
# -------------------------------
class SpecialtyCreate(BaseModel):
    name: str = Field(..., max_length=100)

class SpecialtyResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

# -------------------------------
# Employee View Schema (All Roles)
# -------------------------------
class EmployeeResponse(BaseModel):
    id: UUID
    email: EmailStr
    roles: List[str]
    doctor_profile: Optional[DoctorResponse]
    nurse_profile: Optional[NurseResponse]
    staff_profile: Optional[StaffResponse]

    class Config:
        orm_mode = True

class StaffUpdate(BaseModel):
    department: Optional[str]

class NurseUpdate(BaseModel):
    department: Optional[str]

