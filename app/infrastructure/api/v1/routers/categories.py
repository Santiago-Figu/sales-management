from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.application.services.category_service import CategoryService
from app.infrastructure.api.v1.schemas.categories import(
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema
)

router = APIRouter(prefix="/categories", tags=['Categories'])

@router.post("/", response_model = CategoryResponseSchema)
def create_category(category: CategoryCreateSchema):
    category_data = category.model_dump()
    return CategoryService.create_category(category_data)

@router.get("/{category_id}", response_model = CategoryResponseSchema)
def read_category(category_id: int):
    category = CategoryService.get_category(category_id)
    if not category:
        raise HTTPException(status_code = 404, detail = "category not found")
    return category

@router.get("/", response_model=List[CategoryResponseSchema])
def read_all_categories():
    return CategoryService.get_all_categories()

@router.put("/{category_id}", response_model=CategoryResponseSchema)
def update_category(category_id: int, category: CategoryUpdateSchema):
    category_data = category.model_dump(exclude_unset=True)
    update_category = CategoryService.update_category(category_id, category_data)
    if not update_category:
        raise HTTPException(status_code=404, detail="category not found")
    return update_category

@router.delete("/{category_id}")
def delete_category(category_id: int):
    success = CategoryService.delete_category(category_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "category not found")
    response = {"message": "category deleted successfully"}
    return JSONResponse(content = response, status_code = 200)