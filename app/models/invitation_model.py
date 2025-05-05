from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Invitation(Base):
    __tablename__ = "invitation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inviter_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    invitee_email = Column(String, nullable=False)
    qr_code_url = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending or accepted

    # ✅ Add this relationship
    inviter = relationship("User", back_populates="invitations_sent")
