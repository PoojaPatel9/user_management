from pathlib import Path
from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ✅ Email (Mailtrap)
    smtp_server: str = Field(default='smtp.mailtrap.io', description="SMTP server")
    smtp_port: int = Field(default=2525, description="SMTP port")
    smtp_username: str = Field(default='your-mailtrap-username', description="SMTP username")
    smtp_password: str = Field(default='your-mailtrap-password', description="SMTP password")

    # ✅ Token / Auth
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_minutes: int = Field(default=1440)
    secret_key: str = Field(default="secret-key")
    algorithm: str = Field(default="HS256")
    jwt_secret_key: str = Field(default="a_very_secret_key")
    jwt_algorithm: str = Field(default="HS256")
    max_login_attempts: int = Field(default=5)

    # ✅ Server + App Behavior
    server_base_url: AnyUrl = Field(default="http://localhost:8000")
    invite_base_url: str = Field(default="http://localhost:8000")
    server_download_folder: str = Field(default="downloads")
    debug: bool = Field(default=False)

    # ✅ MinIO Storage
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    # ✅ Admin Credentials
    admin_user: str = Field(default="admin")
    admin_password: str = Field(default="secret")

    # ✅ PostgreSQL Config
    database_url: str = Field(default='postgresql+asyncpg://user:password@postgres/myappdb')
    postgres_user: str = Field(default='user')
    postgres_password: str = Field(default='password')
    postgres_server: str = Field(default='localhost')
    postgres_port: str = Field(default='5432')
    postgres_db: str = Field(default='myappdb')

    # ✅ Optional: External integrations
    discord_bot_token: str = Field(default="NONE")
    discord_channel_id: int = Field(default=1234567890)
    openai_api_key: str = Field(default="NONE")
    send_real_mail: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# ✅ Only one instance created
settings = Settings()
