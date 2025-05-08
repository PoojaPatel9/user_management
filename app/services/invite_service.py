from app.models.invitation_model import Invitation
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.qr_generator import generate_qr_code
from app.utils.minio_client import upload_qr
from app.services.email_service import EmailService
from app.models.user_model import User
from app.schemas.invite_schemas import InviteRequest
from settings.config import Settings
import base64
from sqlalchemy import select
from fastapi import HTTPException, status

async def create_invite(
    db: AsyncSession,
    invite_data: InviteRequest,
    inviter: User,
    email_service: EmailService,
    settings: Settings
):
    # Validation 1: Prevent self-invite
    if invite_data.email == inviter.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot invite yourself."
        )

    # Validation 2: Prevent duplicate pending invite
    result = await db.execute(
        select(Invitation).where(
            Invitation.invitee_email == invite_data.email,
            Invitation.status == "pending"
        )
    )
    existing_invite = result.scalars().first()
    if existing_invite:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An active invite has already been sent to this email."
        )

    # Encode invitee email for QR code reference
    encoded_email = base64.urlsafe_b64encode(invite_data.email.encode()).decode()

    # Generate QR code with reference
    buffer = generate_qr_code(encoded_email, settings.invite_base_url)
    qr_url = upload_qr(buffer)

    # Create Invitation
    invite = Invitation(
        inviter_id=inviter.id,
        invitee_email=invite_data.email,
        qr_code_url=qr_url,
        status="pending",
        accepted=False
    )

    db.add(invite)
    await db.commit()
    await db.refresh(invite)

    # Send invitation email
    await email_service.send_user_email({
        "name": inviter.first_name,
        "email": invite_data.email,
        "qr_code_url": qr_url
    }, 'email_verification')

    return invite
