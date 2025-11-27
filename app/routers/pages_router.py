from fastapi import Request, APIRouter, status, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from db import get_db
from models import Product
from fastapi.responses import HTMLResponse,FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get("/",response_class=HTMLResponse)
async def index_page(request:Request):
    return templates.TemplateResponse('index.html', {"request":request})

@router.get("/catalog",response_class=HTMLResponse)
async def catalog(request: Request, db: AsyncSession = Depends(get_db)):
    query = select(Product)
    result = await db.execute(query)
    products = result.scalars().all()
    
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return templates.TemplateResponse("katalog.html", {
        "request": request,
        "products": products,
    })


@router.get("/robots.txt",response_class=FileResponse)
async def robots():
    return FileResponse('../../visitka2/robots.txt')


@router.get("/sitemap.xml",response_class=FileResponse)
async def sitemap():
    return FileResponse('../../visitka2/sitemap.xml')
