from pydantic import BaseModel, EmailStr
from uuid import UUID

class InviteRequest(BaseModel):
    email: EmailStr

class InviteResponse(BaseModel):
    id: UUID
    invitee_email: EmailStr
    qr_code_url: str
    accepted: bool
