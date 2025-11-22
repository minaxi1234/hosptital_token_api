import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TokenStatus(str, enum.Enum):
    waiting = "waiting"
    completed = "completed"

class Token(Base):
    __tablename__ = "tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_number = Column(String, nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)
    status = Column(Enum(TokenStatus), default=TokenStatus.waiting)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="tokens")
    doctor = relationship("Doctor", back_populates="tokens")
