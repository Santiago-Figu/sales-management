from pydantic import BaseModel
from typing import Optional

class ProductBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    # supplier_id: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    # supplier_id: Optional[int] = None

class ProductResponseSchema(ProductBaseSchema):
    id: int
    
    class Config:
        from_attributes = True