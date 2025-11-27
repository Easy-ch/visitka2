from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db   
from models import  Product, ProductImage
from sqlalchemy import select
from typing import List
from pathlib import Path
import uuid
import shutil

admin_router = APIRouter()



@admin_router.post('/add_product_post', status_code=status.HTTP_201_CREATED)
async def add_product(
    images: List[UploadFile] = File(...),
    name: str = Form(...),
    description: str = Form(...),
    specifications: str = Form(...),
    price: float = Form(...),
    is_available: bool = Form(...),
    advantages: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        image_paths = []
        for file in images:
            upload_dir = Path(f"static/img/products/{file.filename}")
            existing_image_query = select(ProductImage).where(ProductImage.image_path == str(upload_dir))
            existing_image_result = await db.execute(existing_image_query)
            existing_image = existing_image_result.scalar_one_or_none()
            if existing_image or upload_dir.exists():
                unique_id = uuid.uuid4().hex[:8]

                dot_index = file.filename.rfind(".")

                if dot_index != -1:
                    name_without_extension = file.filename[:dot_index]
                    extension = file.filename[dot_index + 1:]
                    upload_dir = Path(f"static/img/products/{name_without_extension}_{unique_id}.{extension}")
            with open(upload_dir, "wb") as f:
                shutil.copyfileobj(file.file, f)
            image_paths.append(upload_dir)
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
        
        for image_path in image_paths:
            new_image = ProductImage(
                product_id=new_product.id,
                image_path=str(image_path)
            )
            db.add(new_image)

        await db.commit()
        await db.refresh(new_product)

        return {
            "message": "Товар успешно добавлен", 
            "product": new_product
        }
    
    except IsADirectoryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при добавлении товара: добавьте хотя бы одно изображение")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при добавлении товара: {str(e)}")