import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user_role import user_roles_table
from app.models.role_permission import role_permissions_table

class Role(Base):
  __tablename__ = "roles"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(100), unique=True, nullable=False, index=True)
  description = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

  users = relationship("User", secondary=user_roles_table, back_populates="roles")
  permissions = relationship("Permission", secondary=role_permissions_table, back_populates="roles")

  def __repr__(self) -> str:
    return f"<Role id={self.id} name={self.name}>"

