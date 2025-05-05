from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
from app.base import Base

from sqlalchemy import Boolean

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inviter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    invitee_email = Column(String, nullable=False)
    qr_code_url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    accepted = Column(Boolean, default=False)  # ✅ Add this field
    created_at = Column(DateTime, default=datetime.utcnow)

    inviter = relationship("User", back_populates="invitations_sent")
