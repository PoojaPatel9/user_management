from app.utils.qr_generator import generate_qr_code
from app.utils.minio_client import upload_qr

nickname = "testuser"
invite_url = "http://localhost:8000/accept-invite/testtoken"

buffer = generate_qr_code(nickname, invite_url)
url = upload_qr(buffer)
print("✅ Uploaded QR Code URL:", url)
