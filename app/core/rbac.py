from typing import List
from fastapi import Depends, HTTPException
from app.core.auth import get_current_user
from app.models.user import User
from uuid import UUID

def require_roles(required_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return current_user

    return role_checker  

   