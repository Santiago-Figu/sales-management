from datetime import datetime
from pydantic import BaseModel, field_serializer
from typing import Optional
from app.infrastructure.api.v1.schemas.categories import CategoryBaseSchema
from app.utils.datatime_utils import format_datetime_with_timezone

class ProductBaseSchema(BaseModel):
    name: str = "Nombre del producto"
    description: str = "Descripción del producto"
    price: float = 0.0
    base_currency: str = "MXN"
    internal_code: str = "00001"
    code: Optional[str] = None
    stock: Optional[int] = 0
    stock_min: Optional[int] = 0
    active: Optional[bool] = True
    category_id: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    base_currency: Optional[str] = None
    internal_code: Optional[str] = None
    code: Optional[str] = None
    stock: Optional[int] = None
    stock_min: Optional[int] = None
    active: Optional[bool] = True
    category_id: Optional[int] = None

class ProductResponseSchema(ProductBaseSchema):
    id: int
    categories: Optional[CategoryBaseSchema] = None
    created: datetime
    last_update: datetime

    @field_serializer('created', 'last_update')
    def serialize_datetime(self, dt: datetime, _info) -> str:
        
        return format_datetime_with_timezone(
            dt,
            timezone_str="America/Mexico_City",
            format_str="%d/%m/%Y %H:%M"
        )
    
    class Config:
        from_attributes = True
