from builtins import Exception
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

# Load environment variables from .env
load_dotenv()

SMTP_SERVER = os.getenv("smtp_server")
SMTP_PORT = int(os.getenv("smtp_port", 2525))
SMTP_USERNAME = os.getenv("smtp_username")
SMTP_PASSWORD = os.getenv("smtp_password")


def send_test_email():
    try:
        msg = MIMEText("This is a test email sent from FastAPI using Mailtrap.")
        msg["Subject"] = "Mailtrap Test Email"
        msg["From"] = SMTP_USERNAME
        msg["To"] = "test@example.com"

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
            print("✅ Test email sent successfully to Mailtrap.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")


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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup logic
@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

    print(f"📡 Mailtrap configured: {SMTP_SERVER}:{SMTP_PORT} as {SMTP_USERNAME}")
    send_test_email()


# Global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

# Include routers
app.include_router(user_routes.router)
