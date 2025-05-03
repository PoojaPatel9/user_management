import requests

invite_payload = {
    "email": "newuser@example.com"
}

headers = {
    "Authorization": "Bearer YOUR_ADMIN_JWT_TOKEN"  # Replace with real token
}

response = requests.post("http://localhost:8000/invite", json=invite_payload, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
