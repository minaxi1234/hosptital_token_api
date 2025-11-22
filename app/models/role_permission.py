# app/models/role_permission.py
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

metadata = Base.metadata

role_permissions_table = Table(
    "role_permissions",
    metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)
