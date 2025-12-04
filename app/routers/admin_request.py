from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db   
from models import  Product, ProductImage
from sqlalchemy import select
from typing import List,Optional
from pathlib import Path
import uuid
import shutil

admin_router = APIRouter()

@admin_router.post('/add_product_post', status_code=status.HTTP_201_CREATED)
async def add_product(
    images: Optional[List[UploadFile]] = File(None),
    name: str = Form(...),
    description: str = Form(...),
    specifications: str = Form(...),
    price: float = Form(...),
    is_available: bool = Form(...),
    advantages: str = Form(""),
    db: AsyncSession = Depends(get_db)
):
    try:
        new_product = Product(
            name=name,
            description=description,
            specifications=specifications,
            price=price,
            advantages=advantages,
            is_available=is_available
        )
        db.add(new_product)
        await db.flush()
        
        valid_images = []
        if images:
            for file in images:
                if file.filename and file.filename.strip():
                    valid_images.append(file)
        
        if valid_images:
            upload_dir = Path("static/img/products")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            for file in valid_images:
                unique_id = uuid.uuid4().hex[:8]
                file_extension = Path(file.filename).suffix
                new_filename = f"{unique_id}{file_extension}"
                file_path = upload_dir / new_filename
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                product_image = ProductImage(
                    product_id=new_product.id,
                    image_path=str(file_path)
                )
                db.add(product_image)
        
        await db.commit()
        await db.refresh(new_product)
        
        return {
            "message": "Товар успешно добавлен",
            "product_id": new_product.id,
            "images_count": len(valid_images) if valid_images else 0
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при добавлении товара: {str(e)}"
        )