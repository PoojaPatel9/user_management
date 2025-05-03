from http.client import HTTPException
import select
from fastapi import APIRouter, Depends
from app.schemas.invite_schemas import InviteRequest, InviteResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user, get_email_service
from app.services.invite_service import create_invite
from app.models.user_model import User

router = APIRouter()

@router.post("/invite", response_model=InviteResponse)
async def invite_user(invite_data: InviteRequest, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user),
                      email_service = Depends(get_email_service)):
    return await create_invite(db, invite_data, current_user, email_service)

@router.get("/accept-invite")
async def accept_invite(ref: str, db: AsyncSession = Depends(get_db)):
    import base64
    from app.models.invitation_model import Invitation
    nickname = base64.urlsafe_b64decode(ref.encode()).decode()
    invite = await db.execute(select(Invitation).join(User).filter(User.nickname == nickname))
    invitation = invite.scalars().first()
    if invitation:
        invitation.accepted = True
        await db.commit()
        return {"message": "Invitation accepted"}
    raise HTTPException(status_code=404, detail="Invalid invite")
