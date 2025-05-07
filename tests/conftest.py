from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from faker import Faker

from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate

fake = Faker()
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

@pytest.mark.asyncio
async def test_example():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/docs")
        assert response.status_code == 200

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope="function")
async def async_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

@pytest.fixture(scope="function")
async def user(db_session):
    data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**data)
    db_session.add(user)
    await db_session.commit()
    return user



@pytest.fixture(scope="function")
async def unverified_user(db_session):
    data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def locked_user(db_session):
    data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": True,
        "failed_login_attempts": settings.max_login_attempts,
    }
    user = User(**data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user = User(
        nickname="admin_user",
        email="admin@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.ADMIN,
        email_verified=True,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def manager_user(db_session: AsyncSession):
    user = User(
        nickname="manager_user",
        email="manager@example.com",
        first_name="Jane",
        last_name="Doe",
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.MANAGER,
        email_verified=True,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

# Token Fixtures
@pytest.fixture
async def admin_token(admin_user):
    return create_access_token(data={"sub": str(admin_user.id), "role": admin_user.role.name})

@pytest.fixture
async def manager_token(manager_user):
    return create_access_token(data={"sub": str(manager_user.id), "role": manager_user.role.name})

@pytest.fixture
async def user_token(user):
    return create_access_token(data={"sub": str(user.id), "role": user.role.name})

# Email Mock
@pytest.fixture
def email_service():
    if settings.send_real_mail == "true":
        return EmailService()
    else:
        mock = AsyncMock(spec=EmailService)
        mock.send_verification_email = AsyncMock(return_value=None)
        mock.send_user_email = AsyncMock(return_value=None)
        return mock

# ✅ FIXED: Users will be created with AUTHENTICATED role
@pytest.fixture
async def users_with_same_role_50_users(db_session, email_service):
    users = []
    for i in range(50):
        user_data = UserCreate(
            email=f"user{i}@test.com",
            password="StrongPass123!",
            nickname=f"user{i}",
            first_name="Test",
            last_name="User",
            role="AUTHENTICATED"  # Pass as string; UserService converts to Enum
        )
        user = await UserService.create(db_session, user_data, email_service)
        users.append(user)
    return users

@pytest.fixture(scope="function")
async def verified_user(db_session):
    data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**data)
    db_session.add(user)
    await db_session.commit()
    return user
