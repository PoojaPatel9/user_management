# User Management System — Final Project @ NJIT

Welcome to the **User Management System Final Project**, an epic open-source adventure crafted by Professor Keith Williams for NJIT’s software engineering students!  
This repository represents my completed journey through implementing new features, resolving real issues, and contributing production-ready code like a professional developer.

---

## Chosen Feature: QR Code Generation User Invites with MinIO

### Feature Description:
This feature allows registered users to invite others via email using a base64-encoded QR code. The QR code encodes a unique reference string to identify the inviter, track successful invitations, and redirect the invitee upon acceptance.

### Key Capabilities:
- Invite users via `/invite` endpoint by entering their email.
- Generate a base64-encoded QR code for each invitation.
- Store QR codes in **MinIO** via Docker.
- Track invite status (`pending`, `accepted`) in a dedicated table.
- Accept invites via `/invite/accept?ref=...`, marking them as used.
- View personal invite stats via `/me/invites`.
- Administer invitations via a full BREAD HATEOS-style API.

---

## QA Issues Resolved

| Issue # | Title |
|--------|-------|
| [#1](https://github.com/PoojaPatel9/user_management/issues/1) | Email verification email was not being sent after registration |
| [#5](https://github.com/PoojaPatel9/user_management/issues/5) | Swagger UI not showing token input box for OAuth2PasswordBearer |
| [#6](https://github.com/PoojaPatel9/user_management/issues/6) | MinIO Service Connection Failure in GitHub Actions During CI/CD |
| [#7](https://github.com/PoojaPatel9/user_management/issues/7) | Missing Test Coverage for Invite API Routes (`/invite`, `/invite/accept`, `/me/invites`) |
| [#8](https://github.com/PoojaPatel9/user_management/issues/8) | Missing Business Rule Validation in `invite_service.py` |

---

## Test Coverage Improvements

I added **10+ tests** to ensure invite functionality works reliably:
- Invite creation with valid email
- Self-invites are rejected (`400 Bad Request`)
- Duplicate invites are blocked (`409 Conflict`)
- Invalid email format returns `422 Unprocessable Entity`
- Invite acceptance updates status
- Invite stats return correct counts

All tests use `pytest`, `httpx.AsyncClient`, and FastAPI dependency overrides.

---

## Business Logic Validations

Added validation in `invite_service.py` to ensure:
- Users **cannot invite themselves**
- Duplicate active invites are **not allowed**
- Only pending invites can be accepted

These rules prevent misuse and ensure the invite system behaves predictably and securely.

---

## CI/CD + DockerHub

- GitHub Actions pipeline with PostgreSQL + MinIO containers
- Fixed MinIO startup timing using Docker + `sleep` and `mc` CLI
- Successfully deploys project Docker image

**DockerHub Repo**: [poojapatel9/user_management](https://hub.docker.com/repository/docker/poojapatel9/user_management)

---

## Reflection

Working on this final project taught me how to approach problems like a real software engineer. I identified real bugs, solved integration issues in CI/CD, enforced business rules, and added meaningful test coverage. Implementing QR Code-based invites helped me understand full-stack integration between databases, file storage (MinIO), backend services, and testing—all while following modern development practices.

---

## Getting Started

```bash
# Clone project
git clone https://github.com/PoojaPatel9/user_management.git
cd user_management

# Start system
docker compose up --build
