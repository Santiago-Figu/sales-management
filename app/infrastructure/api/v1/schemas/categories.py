from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime
from app.utils.datatime_utils import format_datetime_with_timezone

class CategoryBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    active: Optional[bool] = True

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class CategoryResponseSchema(CategoryBaseSchema):
    id: int
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
        from_attributes = True # Anteriormente llamado orm_mode en versiones antiguas