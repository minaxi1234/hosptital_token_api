from sqlalchemy.orm import Session
from app.models.role import Role

DEFAULT_ROLES = ["admin", "doctor", "nurse", "staff"]

def seed_roles(db: Session):

  for role_name in DEFAULT_ROLES:
    existing = db.query(Role).filter(Role.name == role_name).first()
    if not existing:
      db.add(Role(name=role_name))

  db.commit()
