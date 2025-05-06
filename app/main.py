from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

# Internal imports
from app.database import Database
from app.dependencies import get_settings
from app.utils.api_description import getDescription
from app.routers import user_routes, invite_routes # 👈 Include auth routes separately

# 🌐 Load environment variables
load_dotenv()
SMTP_SERVER = os.getenv("smtp_server")
SMTP_PORT = int(os.getenv("smtp_port", 2525))
SMTP_USERNAME = os.getenv("smtp_username")
SMTP_PASSWORD = os.getenv("smtp_password")

# 🚀 FastAPI instance
app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# 🔐 Token Auth - keep token input box
security_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User Management",
        version="0.0.1",
        description=getDescription(),
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {"type": "http", "scheme": "bearer"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"HTTPBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 🌍 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_test_email():
    try:
        msg = MIMEText("This is a test email sent from FastAPI using Mailtrap.")
        msg["Subject"] = "Mailtrap Test Email"
        msg["From"] = SMTP_USERNAME
        msg["To"] = "test@example.com"

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.ehlo()  # Say hello
            try:
                server.starttls()  # Attempt to upgrade the connection to TLS
                server.ehlo()
            except smtplib.SMTPException:
                pass  # Ignore if TLS isn't supported (shouldn't happen with Mailtrap)

            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())

        print("✅ Test email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

# ⚙️ App startup
@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)
    print(f"📡 Mailtrap configured: {SMTP_SERVER}:{SMTP_PORT} as {SMTP_USERNAME}")
    send_test_email()

# ❗ Global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

# 📌 Include Routers
#app.include_router(auth_routes.router, tags=["Login and Registration"])
app.include_router(user_routes.router, tags=["User Management (Admin or Manager Roles)"])
app.include_router(invite_routes.router, tags=["Invites"])
