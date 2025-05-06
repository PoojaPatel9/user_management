from app.models.invitation_model import Invitation
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.qr_generator import generate_qr_code
from app.utils.minio_client import upload_qr
from app.services.email_service import EmailService
from app.models.user_model import User
from app.schemas.invite_schemas import InviteRequest
from settings.config import Settings
import base64

async def create_invite(
    db: AsyncSession,
    invite_data: InviteRequest,
    inviter: User,
    email_service: EmailService,
    settings: Settings
):
    # ✅ Encode invitee email for QR code reference
    encoded_email = base64.urlsafe_b64encode(invite_data.email.encode()).decode()

    # ✅ Generate QR code with reference
    buffer = generate_qr_code(encoded_email, settings.invite_base_url)
    qr_url = upload_qr(buffer)

    # ✅ Create Invitation with status explicitly set to pending
    invite = Invitation(
        inviter_id=inviter.id,
        invitee_email=invite_data.email,
        qr_code_url=qr_url,
        status="pending",           # ✅ Required for /invite/accept to find it
        accepted=False              # ✅ Make sure it's not accepted yet
    )

    db.add(invite)
    await db.commit()
    await db.refresh(invite)

    # ✅ Send invitation email with QR code link
    await email_service.send_user_email({
        "name": inviter.first_name,
        "email": invite_data.email,
        "qr_code_url": qr_url
    }, 'email_verification')

    return invite
