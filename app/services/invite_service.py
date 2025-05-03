from app.models.invitation_model import Invitation
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.qr_generator import generate_qr_code
from app.utils.minio_client import upload_qr
from app.services.email_service import EmailService
from app.models.user_model import User
from app.schemas.invite_schemas import InviteRequest

async def create_invite(db: AsyncSession, invite_data: InviteRequest, inviter: User, email_service: EmailService):
    buffer = generate_qr_code(inviter.nickname, settings.invite_base_url)
    qr_url = upload_qr(buffer)

    invite = Invitation(inviter_id=inviter.id, invitee_email=invite_data.email, qr_code_url=qr_url)
    db.add(invite)
    await db.commit()
    await db.refresh(invite)

    await email_service.send_user_email({
        "name": inviter.first_name,
        "email": invite_data.email,
        "qr_code_url": qr_url
    }, 'email_verification')

    return invite
