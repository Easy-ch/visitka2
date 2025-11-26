from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from config import SECRET_KEY
from utils import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from db import async_engine
from models import Product
from models import SuperUser
from sqlalchemy import select
from db import async_engine
import logging



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)




class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with AsyncSession(async_engine) as db:
            query = select(SuperUser).where(SuperUser.username == username)
            result = await db.execute(query)
            user = result.scalar_one_or_none()

            if not user or not verify_password(password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверные учетные данные"
                )
            request.session["user_id"] = user.id

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if not user_id:
            return False

        async with AsyncSession(async_engine) as db:
            result = await db.execute(select(SuperUser).where(SuperUser.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return False

        return True

authentication_backend = AdminAuth(secret_key=SECRET_KEY)
