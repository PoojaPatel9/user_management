from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        try:
            html_content = self.template_manager.render_template(email_type, **user_data)
            self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])
            logger.info(f"✅ Email sent to {user_data['email']} for {email_type}")
        except Exception as e:
            logger.error(f"❌ Failed to send {email_type} email to {user_data['email']}: {e}")

    async def send_verification_email(self, user: User):
        # Build the verification URL
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"

        # Optionally create a QR code version (for now just use the same URL in both)
        qr_code_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"

        print(f"📧 Sending verification to {user.email} with URL: {verification_url}")

        await self.send_user_email({
            "name": user.first_name,
            "email": user.email,
            "verification_url": verification_url,
            "qr_code_url": qr_code_url  # ✅ Add this for use in template
        }, 'email_verification')
