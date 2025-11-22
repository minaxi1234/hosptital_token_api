from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import List, Optional


# ----------- Login Request -----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ----------- Token Response -----------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ----------- Token Payload inside JWT -----------
class TokenPayload(BaseModel):
    user_id: UUID
    roles: List[str]
    exp: int


# ----------- Refresh Request -----------
class RefreshRequest(BaseModel):
    refresh_token: str


# ----------- User Response -----------
class UserCreate(BaseModel):
    email: EmailStr
    roles: List[str]
    is_active: bool
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    roles: List[str]
    is_active: bool
    
    @classmethod
    def from_orm(cls, user):
        return cls(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            roles=[role.name for role in user.roles]   #  ← FIX
        )


    class Config:
        from_attributes = True


# ----------- Role Response -----------
class RoleResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True
