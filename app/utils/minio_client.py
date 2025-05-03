from minio import Minio
from io import BytesIO
import uuid
from settings.config import settings

minio_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False
)

def upload_qr(buffer: BytesIO) -> str:
    filename = f"{uuid.uuid4()}.png"
    minio_client.put_object(
        settings.minio_bucket,
        filename,
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="image/png"
    )
    return f"http://{settings.minio_endpoint}/{settings.minio_bucket}/{filename}"
