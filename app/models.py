from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from sqlalchemy import Index
from sqladmin import ModelView


Base = declarative_base()



class SuperUser(Base):
    __tablename__ = 'superuser'
    id = Column(Integer,primary_key=True,unique=True)
    username = Column(String,unique=True)
    password = Column(String,nullable=False)

    def __str__(self):
        return self.username

class Product(Base):
    __tablename__ = "products"

    id             = Column(Integer, primary_key=True, index=True,autoincrement=True)                # id товара
    name           = Column(String, nullable=False)                               # Название товара
    description    = Column(Text, nullable=True)                                  # Описание товара
    specifications = Column(Text, nullable=True)                                  # Характеристики
    price          = Column(Float, nullable=False)                                # Цена
    advantages     = Column(Text, nullable=True)                                  # Преимущества
    is_available   = Column(Boolean, nullable=False, default=True)                # Наличие


    images         = relationship("ProductImage", back_populates="product", lazy="selectin", cascade="all, delete-orphan")
    def __str__(self):
        return self.name

class ProductImage(Base):
    __tablename__ = "product_images"

    id         = Column(Integer, primary_key=True, index=True,autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id",ondelete="CASCADE"), nullable=False) # Ссылка на товар
    image_path = Column(String, nullable=True)                             # Путь к изображению
    product = relationship("Product", back_populates="images", lazy="selectin")


