from fastapi import Request, APIRouter, status, Depends, HTTPException, Query
from fastapi.templating import Jinja2Templates
from db import get_db
from pathlib import Path
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory='templates')
# templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

@router.get("/",response_class=HTMLResponse)
async def index_page(request:Request):
    return templates.TemplateResponse('index.html', {"request":request})