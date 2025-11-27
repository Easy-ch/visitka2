from passlib.context import CryptContext
from fastapi import HTTPException, status
from passlib.context import CryptContext
import aiohttp


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def send_message(token, chat_id, message):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        async with session.post(url, params=params) as response:
            return await response.json()
