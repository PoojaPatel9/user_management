from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
import base64
from sqlalchemy.orm import joinedload
from app.schemas.invite_schemas import InviteRequest, InviteResponse
from app.dependencies import get_db, get_current_user, get_email_service, get_settings
from app.services.invite_service import create_invite
from app.models.user_model import User
from app.models.invitation_model import Invitation
from settings.config import Settings

router = APIRouter()


@router.post("/invite", response_model=InviteResponse)
async def invite_user(
    invite_data: InviteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    email_service=Depends(get_email_service),
    settings: Settings = Depends(get_settings),  # ✅ inject config here
):
    return await create_invite(db, invite_data, current_user, email_service, settings)


@router.get("/invite/accept")
async def accept_invite(
    ref: str,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    import base64

    try:
        nickname = base64.urlsafe_b64decode(ref.encode()).decode()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid reference string")

    # ✅ Join User table and filter by nickname
    result = await db.execute(
        select(Invitation)
        .join(User, User.id == Invitation.inviter_id)
        .where(
            and_(
                User.nickname == nickname,
                Invitation.status == "pending"
            )
        )
    )
    invite = result.scalars().first()

    if invite:
        invite.status = "accepted"
        await db.commit()
        return RedirectResponse(url=settings.invite_base_url)

    raise HTTPException(status_code=404, detail="Invite not found")

@router.get("/me/invites")
async def get_my_invites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Invitation).where(Invitation.inviter_id == current_user.id)
    )
    invites = result.scalars().all()
    sent = len(invites)
    accepted = sum(1 for i in invites if i.status == "accepted")
    return {"sent": sent, "accepted": accepted}