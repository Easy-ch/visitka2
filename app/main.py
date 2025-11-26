from fastapi import FastAPI,HTTPException,Request, Depends
from pathlib import Path
from db import get_db,async_engine,init_db
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
from sqladmin import Admin
from admin import authentication_backend
from fastapi.middleware.cors import CORSMiddleware
from routers.pages_router import router
# from admin import authentication_backend


# class StaticFilesWithoutCaching(StaticFiles):
#     def is_not_modified(self, *args, **kwargs) -> bool:
#         return super().is_not_modified(*args, **kwargs) and False

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, async_engine,authentication_backend=authentication_backend,favicon_url = "/static/img/admin-logo.ico",title='Админ',base_url='/arhremprint_admin')

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

green = "\033[32m"
reset = "\033[0m"

app.include_router(router)


origins = [
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать конкретные домены, если нужно
    allow_credentials=True,
    allow_methods=["*"],  # Или указать только методы, которые должны быть разрешены
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, proxy_headers=True)