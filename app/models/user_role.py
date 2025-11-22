from datetime import datetime
from sqlalchemy import Table,  Column , ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


metadata = Base.metadata

user_roles_table = Table(
  "user_roles",
  metadata,
  Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
  Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
  Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
  Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)

