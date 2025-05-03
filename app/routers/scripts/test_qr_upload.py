from app.utils.minio_client import upload_qr
from app.utils.qr_generator import generate_qr_code

# Generate QR Code for nickname + redirect URL
qr_buffer = generate_qr_code("testuser", "http://localhost:8000/accept-invite?ref=test_ref")

# Upload to MinIO
url = upload_qr(qr_buffer)
print("Uploaded QR Code URL:", url)
