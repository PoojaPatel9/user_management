import requests

invite_payload = {
    "email": "newuser@example.com"
}
headers = {
    "Authorization": "Bearer YOUR_ADMIN_JWT_TOKEN"
}

response = requests.post("http://localhost:8000/invite", json=invite_payload, headers=headers)
print(response.status_code)
print(response.json())
