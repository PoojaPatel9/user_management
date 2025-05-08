# 👥 User Management System — Final Project @ NJIT

Welcome to the **User Management System Final Project** — a collaborative, test-driven, and real-world software engineering experience designed by Professor Keith Williams for NJIT's brightest software developers. This repository represents my personal journey and contribution to this epic coding adventure. 🧠💻🚀

---

## 🔥 Project Highlights

- ✅ **5 QA Issues Identified & Resolved**
- ✅ **10+ New Tests Written**
- ✅ **1 Major Feature Implemented: QR Code Invitation with Minio**
- ✅ **Deployed to DockerHub**
- ✅ **CI/CD via GitHub Actions**

🔗 **GitHub Repository:** [user_management](https://github.com/PoojaPatel9/user_management.git)  
🐳 **DockerHub Image:** [poojapatel9/user_management](https://hub.docker.com/repository/docker/poojapatel9/user_management)

---

## 🎯 Project Goals

- Get hands-on **real-world experience** with API development.
- Practice **Quality Assurance** through detailed issue tracking and testing.
- Improve **test coverage** by writing tests for edge cases and core features.
- Develop and document a **new feature** using best practices.
- Collaborate using GitHub issues, commits, and PRs like a professional.
- Deliver a **production-ready** project deployed via Docker.

---

## 🚀 New Feature: QR Code Generation for User Invites 🎫

**Feature Title:** QR Code Generation User Invites with Minio  
**Difficulty:** Medium  
**Status:** ✅ Complete  
**User Story:**  
> As a user, I want to invite others via email, each with a unique QR code that tracks the invitation, so they can join easily by scanning.

### ✅ Feature Capabilities

- Invites users via email using a secure API endpoint.
- Each invitation email includes a **base64-encoded QR code** linking back to the inviter.
- Tracks invite status (sent, accepted) in a dedicated database table.
- Stores QR code images in **Minio Object Storage** (Docker-based).
- Admins can manage invitations via a full **BREAD HATEOAS API**.
- Supports `.env` configuration for QR forwarding URLs and email behavior.

### 🛠️ Technical Highlights

- 🔐 **Secure Invite Token Generation**
- 🖼️ **Base64 QR Code Image Generation**
- 📦 **Minio Integration** for storing QR images
- ✅ **API Endpoints** for:
  - Sending invitations
  - Accepting invitations
  - Viewing invite stats
  - Admin CRUD operations for invite management
- 📬 **EmailService** extension for sending QR invites
- 🧪 **Extensive unit + integration testing**

---

## 🐞 QA Issues Resolved

All issues were logged, fixed, and closed on GitHub with full traceability:

| Issue # | Title | Description |
|--------|-------|-------------|
| [#1](https://github.com/PoojaPatel9/user_management/issues/1) | Username Validation | Restrict special characters, enforce length |
| [#2](https://github.com/PoojaPatel9/user_management/issues/2) | Password Strength | Enforce strong password rules |
| [#3](https://github.com/PoojaPatel9/user_management/issues/3) | Profile Update Error | Validate optional fields in update API |
| [#4](https://github.com/PoojaPatel9/user_management/issues/4) | Swagger Token Input | Fixed HTTPBearer input in Swagger UI |
| [#5](https://github.com/PoojaPatel9/user_management/issues/5) | Email Verification Failing | Solved SMTP error and improved retry |

---

## ✅ Tests Added

To ensure code reliability and edge case handling, 10+ new tests were implemented across:

- 🔒 User registration and login
- ✏️ User update and deletion
- 📩 Email verification and resend
- 🎫 QR invite creation, usage, and tracking
- 📦 Minio upload + retrieval
- 🔄 Admin BREAD endpoints for invitation system

Test files include:
- `tests/test_services/test_user_api.py`
- `tests/test_services/test_invite_api.py`
- `tests/test_schemas/test_user_schemas.py`

---

## 🐳 Docker & CI/CD

- ✔ Dockerized with `docker-compose`
- ✔ Minio service configured with `.env` and `docker-compose.yml`

- ✔ Auto-tests run using **GitHub Actions**
- ✔ Main branch always deployable

**Start Locally**:
```bash
git clone https://github.com/PoojaPatel9/user_management.git
cd user_management
docker compose up --build
