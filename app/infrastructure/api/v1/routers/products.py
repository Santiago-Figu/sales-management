from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.application.services.product_service import ProductService
from app.infrastructure.api.v1.schemas.products import(
    ProductBaseSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema
)

router = APIRouter(prefix="/products", tags=['Products'])

@router.post("/", response_model = ProductBaseSchema)
def create_product(product: ProductCreateSchema):
    product_data = product.model_dump()
    return ProductService.create_product(product_data)

@router.get("/{product_id}", response_model = ProductResponseSchema)
def read_product(product_id: int):
    product = ProductService.get_product(product_id)
    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    return product

@router.get("/", response_model=List[ProductResponseSchema])
def read_all_products():
    return ProductService.get_all_products()

@router.put("/{product_id}", response_model=ProductResponseSchema)
def update_product(product_id: int, product: ProductUpdateSchema):
    product_data = product.model_dump(exclude_unset=True)
    update_product = ProductService.update_product(product_id, product_data)
    if not update_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product

@router.delete("/{product_id}")
def delete_product(product_id: int):
    success = ProductService.delete_product(product_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "Product not found")
    response = {"message": "Product deleted successfully"}
    return JSONResponse(content = response, status_code = 200)