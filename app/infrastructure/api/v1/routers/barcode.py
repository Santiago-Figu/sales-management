from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.application.services.product_service import ProductService
from app.infrastructure.api.v1.schemas.barcode import BarCodeCreate, BarCodeCreateIdProduct, BarCodeResponse
from app.utils.barcode.bar_code import code_product_format, generar_codigo_ean13

router = APIRouter(prefix="/barcodes", tags=['Bar Codes'])

@router.post("/", response_model = BarCodeResponse)
def generate_barcode(barcode_data: BarCodeCreate):
    try:
        bar_code= generar_codigo_ean13(
            codigo_producto=code_product_format(barcode_data.internal_code),
            clave_pais=barcode_data.clave_pais,
            empresa_id=barcode_data.empresa_id
        )
        message = "Código generado correctamente"
        status = 200
        response = {"message":message,"barcode":bar_code}
    except Exception as e:
        status = 400
        message = "Ocurrio un error al generar el código"
        response = {"message":message,"detail":str(e)}

    return JSONResponse(content=response, status_code=status)

@router.post("/generate/{id_product}", response_model = BarCodeResponse)
def generate_barcode_id_product(id_product: int, barcode_data: BarCodeCreateIdProduct):
    try:
        product = ProductService.get_product(id_product)
        if not product:
            raise HTTPException(status_code = 404, detail = "Product not found")
        bar_code= generar_codigo_ean13(
            codigo_producto=code_product_format(product.internal_code),
            clave_pais=barcode_data.clave_pais,
            empresa_id=barcode_data.empresa_id
        )
        
        message = "Código generado correctamente"
        status = 200
        response = {"message":message,"barcode":bar_code}
    except Exception as e:
        status = 400
        message = "Ocurrio un error al generar el código"
        response = {"message":message,"detail":str(e)}

    return JSONResponse(content=response, status_code=status)

@router.post("/create/{id_product}", response_model = BarCodeResponse)
def create_barcode(id_product: int, barcode_data: BarCodeCreateIdProduct):
    try:
        product = ProductService.get_product(id_product)
        if not product:
            raise HTTPException(status_code = 404, detail = "Product not found")
        bar_code= generar_codigo_ean13(
            codigo_producto=code_product_format(product.internal_code),
            clave_pais=barcode_data.clave_pais,
            empresa_id=barcode_data.empresa_id
        )
        product_data = {"code": bar_code}
        ProductService.update_product(id_product,product_data)
        
        message = "Código generado y actualizado correctamente"
        status = 200
        response = {"message":message,"barcode":bar_code}
    except Exception as e:
        status = 400
        message = "Ocurrio un error al generar el código"
        response = {"message":message,"detail":str(e)}

    return JSONResponse(content=response, status_code=status)