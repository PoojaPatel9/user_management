from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import base64
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
    settings: Settings = Depends(get_settings),
):
    """
    Invite a user via email, generate a QR code, and store the invite.
    """

    # 🔐 Validation 1: Prevent self-invite
    if invite_data.email == current_user.email:
        raise HTTPException(
            status_code=400,
            detail="You cannot invite yourself."
        )

    # 🔐 Validation 2: Prevent duplicate pending invite
    result = await db.execute(
        select(Invitation).where(
            Invitation.invitee_email == invite_data.email,
            Invitation.status == "pending"
        )
    )
    existing_invite = result.scalars().first()
    if existing_invite:
        raise HTTPException(
            status_code=409,
            detail="An active invite has already been sent to this email."
        )

    return await create_invite(db, invite_data, current_user, email_service, settings)


@router.get("/invite/accept")
async def accept_invite(
    ref: str,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Accept an invitation using the base64-encoded invitee email as `ref`.
    Marks the invitation as accepted and redirects the user.
    """
    try:
        invitee_email = base64.urlsafe_b64decode(ref.encode()).decode()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid reference string")

    result = await db.execute(
        select(Invitation).where(
            Invitation.invitee_email == invitee_email,
            Invitation.status == "pending"
        )
    )
    invite = result.scalars().first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")

    invite.status = "accepted"
    invite.accepted = True
    await db.commit()

    return {"message": "Invite accepted", "email": invite.invitee_email}


@router.get("/me/invites")
async def get_my_invites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a count of invites sent and accepted by the logged-in user.
    """
    result = await db.execute(
        select(Invitation).where(Invitation.inviter_id == current_user.id)
    )
    invites = result.scalars().all()
    sent = len(invites)
    accepted = sum(1 for i in invites if i.status == "accepted")
    return {"sent": sent, "accepted": accepted}
