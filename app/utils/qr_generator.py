import base64
from io import BytesIO
import qrcode

def generate_qr_code(nickname: str, base_url: str) -> BytesIO:
    ref = base64.urlsafe_b64encode(nickname.encode()).decode()
    full_url = f"{base_url}/accept-invite?ref={ref}"
    qr = qrcode.make(full_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
