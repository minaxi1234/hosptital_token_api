import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import load_dotenv
from argon2 import PasswordHasher

from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.user_role import user_roles_table
from app.core.config import settings

load_dotenv()
ADMIN_EMAIL=settings.ADMIN_EMAIL
ADMIN_PASSWORD=settings.ADMIN_PASSWORD

ph = PasswordHasher()

def create_admin():
  db = SessionLocal()

  try:
    existing_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if existing_user:
      print("Admin already exists.")
      return
    
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
      admin_role = Role(name="admin")
      db.add(admin_role)
      db.commit()
      db.refresh(admin_role)

    hashed_password = ph.hash(ADMIN_PASSWORD)
    admin_user = User(
      email=ADMIN_EMAIL,
      hashed_password=hashed_password,
      is_active=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    db.execute(
      user_roles_table.insert().values(user_id=admin_user.id, role_id=admin_role.id)
    )
    db.commit()
    print("Super admin created successfully")
  except Exception as e:
    print("Error:", e)
    db.rollback()
  finally:
    db.close()

if __name__ == "__main__":
  create_admin()
