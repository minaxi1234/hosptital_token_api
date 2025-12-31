import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user_role import user_roles_table

class User(Base):
  __tablename__ = "users"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  full_name = Column(String(150), nullable=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  phone = Column(String(32), nullable=True, index=True)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
  updated_at = Column(DateTime, default=datetime.utcnow, 
  onupdate=datetime.utcnow, nullable=False)


  roles = relationship(
    "Role",
    secondary=user_roles_table,
    back_populates="users",
    lazy="subquery"  
)
  doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
  nurse_profile = relationship("Nurse", back_populates="user", uselist=False)
  staff_profile = relationship("Staff", back_populates="user", uselist=False)
  

  def __repr__(self) -> str:
    return f"<Uset id={self.id} email = {self.email}>"



