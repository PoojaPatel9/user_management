import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_invite_user_success(async_client: AsyncClient, user_token: str):
    # Act
    response = await async_client.post(
        "/invite",
        json={"email": "newuser@example.com"},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["invitee_email"] == "newuser@example.com"
    assert data["status"] == "pending"
    assert data["accepted"] is False
    assert "qr_code_url" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_invite_self_should_fail(async_client: AsyncClient, user_token: str, user):
    response = await async_client.post(
        "/invite",
        json={"email": user.email},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot invite yourself."

@pytest.mark.asyncio
async def test_duplicate_invite_should_fail(async_client: AsyncClient, user_token: str):
    email = "repeat@example.com"

    # First invite - should succeed
    await async_client.post(
        "/invite",
        json={"email": email},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Second invite - should fail
    response = await async_client.post(
        "/invite",
        json={"email": email},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "An active invite has already been sent to this email."

@pytest.mark.asyncio
async def test_invite_with_invalid_email(async_client: AsyncClient, user_token: str):
    response = await async_client.post(
        "/invite",
        json={"email": "invalid-email"},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 422
