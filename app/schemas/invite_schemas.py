from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class InviteRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user to invite")

class InviteResponse(BaseModel):
    id: UUID
    invitee_email: EmailStr
    qr_code_url: str = Field(..., description="URL to the generated QR code stored in MinIO")
    status: str = Field(..., description="Invitation status: pending or accepted")
    accepted: bool = Field(..., description="Whether the invite was accepted")
    created_at: datetime = Field(..., description="Timestamp when the invite was created")

    class Config:
        orm_mode = True
