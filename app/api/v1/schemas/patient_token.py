from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# -------------------------------
# Patient Schemas
# -------------------------------
class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: int = Field(..., gt=0)
 

class PatientRead(BaseModel):
    id: UUID
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]
    age: int

    class Config:
        orm_mode = True

class PatientInToken(BaseModel):
    id: UUID
    name: str
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        orm_mode = True

# -------------------------------
# Token Schemas
# -------------------------------
class TokenStatus(str, Enum):
    waiting = "waiting"
    in_progress = "in_progress"
    completed = "completed"

class TokenCreate(BaseModel):
    patient_id: UUID
    doctor_id: UUID

class TokenRead(BaseModel):
    id: UUID
    token_number: str
    patient_id: UUID
    doctor_id: UUID
    status: TokenStatus
    created_at: datetime
    patient: Optional[PatientInToken]

    class Config:
        orm_mode = True

class TokenUpdateStatus(BaseModel):
    status: TokenStatus
