from typing import List
from app.api.v1.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserResponse

from app.core.rbac import require_roles
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.session import get_db

from app.core.auth import get_current_user

from app.models.role import Role
from app.utils.hashing import hash_password

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.hashing import verify_password



router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post("/create", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    # 1. Check duplicate email
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    # 2. Create basic user
    new_user = User(
        email=data.email,
        is_active=data.is_active,
        hashed_password=hash_password(data.password),
    )

    db.add(new_user)
    db.commit()         # Write the user first
    db.refresh(new_user)

    # 3. Attach roles (doctor, nurse, staff, admin, etc.)
    roles = db.query(Role).filter(Role.name.in_(data.roles)).all()

    if not roles:
        raise HTTPException(400, detail="Invalid roles")

    new_user.roles = roles
    db.commit()

    # 4. RELOAD user WITH roles from DB
    new_user = (
        db.query(User)
        .filter(User.id == new_user.id)
        .first()
    )

    return UserResponse.from_orm(new_user)



@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    # 1. Check user exists
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 2. Verify password using Argon2
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 3. Create tokens
    access_token = create_access_token({"user_id": str(user.id)})
    refresh_token = create_refresh_token({"user_id": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )



@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: dict = Body(...)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("user_id")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token({"user_id": user_id})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_roles(["admin"]))):
    users = db.query(User).all()

    # convert to safe response objects
    return [UserResponse.from_orm(u) for u in users]



@router.delete("/delete/{user_id}", status_code=200)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Remove role relationships first (avoid orphan rows)
    if user.doctor_profile:
        db.delete(user.doctor_profile)
        db.flush()  # Flush without committing
    
    # Delete nurse profile if exists
    if user.nurse_profile:
        db.delete(user.nurse_profile)
        db.flush()
    
    # Delete staff profile if exists
    if user.staff_profile:
        db.delete(user.staff_profile)
        db.flush()

    # Remove role relationships first
    user.roles.clear()
    db.flush()


    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)
