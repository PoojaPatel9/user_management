import pytest
import base64
from httpx import AsyncClient
from app.main import app
from app.services.email_service import EmailService

# Patch the email service at the object level (instance), not class
@pytest.fixture(autouse=True)
def mock_send_user_email(monkeypatch):
    async def _mock_send_user_email(self, user_data: dict, email_type: str):
        print(f"[MOCKED] Skipping real email to: {user_data['email']} | Type: {email_type}")
        return

    monkeypatch.setattr(EmailService, "send_user_email", _mock_send_user_email)
    
@pytest.mark.asyncio
async def test_invite_user_as_admin(async_client: AsyncClient, admin_token: str):
    response = await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": "test.invitee@example.com"}
    )
    assert response.status_code == 200
    assert "qr_code_url" in response.json()

@pytest.mark.asyncio
async def test_invite_user_unauthorized(async_client: AsyncClient):
    response = await async_client.post("/invite", json={"email": "unauth@example.com"})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_invite_user_missing_email(async_client: AsyncClient, admin_token: str):
    response = await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_my_invites(async_client: AsyncClient, admin_token: str):
    response = await async_client.get(
        "/me/invites",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sent" in data
    assert "accepted" in data

@pytest.mark.asyncio
async def test_invite_accept_redirect(async_client: AsyncClient, admin_token: str):
    email = "accept.invite@example.com"
    encoded_email = base64.urlsafe_b64encode(email.encode()).decode()

    await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": email}
    )

    response = await async_client.get(f"/invite/accept?ref={encoded_email}")
    assert response.status_code in (200, 307)

@pytest.mark.asyncio
async def test_accept_invalid_invite(async_client: AsyncClient):
    response = await async_client.get("/invite/accept?ref=invalidstring")
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_invite_duplicate_email(async_client: AsyncClient, admin_token: str):
    email = "duplicate@example.com"

    await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": email}
    )

    response = await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": email}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_qr_code_url_format(async_client: AsyncClient, admin_token: str):
    response = await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": "qr.format@example.com"}
    )
    qr_url = response.json().get("qr_code_url", "")
    assert qr_url.startswith("http://") or qr_url.startswith("https://")

@pytest.mark.asyncio
async def test_invite_counts(async_client: AsyncClient, admin_token: str):
    response = await async_client.get(
        "/me/invites",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    data = response.json()
    assert isinstance(data["sent"], int)
    assert isinstance(data["accepted"], int)

@pytest.mark.asyncio
async def test_invite_invalid_email_format(async_client: AsyncClient, admin_token: str):
    response = await async_client.post(
        "/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": "not-an-email"}
    )
    assert response.status_code == 422
