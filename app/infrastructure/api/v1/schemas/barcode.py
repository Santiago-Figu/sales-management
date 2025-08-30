from pydantic import BaseModel, field_serializer
from typing import Optional
from app.core.barcode.bar_code import code_product_format

class BarCodeBaseSchema(BaseModel):
    internal_code: str = "00342"

    @field_serializer('internal_code')
    def serialize_internal_code(self, code: str) -> str:
        return code_product_format(code_product=code, longitud=5)

class BarCodeCreate(BarCodeBaseSchema):
    clave_pais:  Optional[int] = 750
    empresa_id:  Optional[str] = "99999"  # ID genérico para pruebas

class BarCodeCreateIdProduct(BaseModel):
    clave_pais:  Optional[int] = 750
    empresa_id:  Optional[str] = "99999"  # ID genérico para pruebas

class BarCodeResponse(BaseModel):
    barcode: str = "75099999003420"

class BarCodeImgResponse(BarCodeBaseSchema):
    img: str