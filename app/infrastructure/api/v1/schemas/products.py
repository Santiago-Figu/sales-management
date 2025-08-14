from pydantic import BaseModel
from typing import Optional
from app.infrastructure.api.v1.schemas.categories import CategoryBaseSchema

class ProductBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    category_id: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponseSchema(ProductBaseSchema):
    id: int
    categories: Optional[CategoryBaseSchema] = None
    class Config:
        from_attributes = True
