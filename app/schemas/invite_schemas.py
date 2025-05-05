from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class InviteRequest(BaseModel):
    email: EmailStr

class InviteResponse(BaseModel):
    id: UUID
    invitee_email: EmailStr
    qr_code_url: str
    status: str
    accepted: bool  # ✅ Add this field
    created_at: datetime

    class Config:
        orm_mode = True
