from pydantic import BaseModel
from typing import Optional

class CategoryBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponseSchema(CategoryBaseSchema):
    id: int
    class Config:
        from_attributes = True