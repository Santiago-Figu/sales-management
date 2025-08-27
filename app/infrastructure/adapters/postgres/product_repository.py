from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository
from app.infrastructure.database.postgres import get_db

class PostgresProductRepository(ProductRepository):
    def __init__(self, db: Session):
        self.db = db
    
    # Operaciones de CRUD básicas

    def create(self, product: Product) -> Product:
        
        self._validate_internal_code(product.internal_code)
        self._validate_code(product.code)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_by_id(self, product_id:int) -> Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.categories))
            .filter(Product.id == product_id)
            .first()
        )
    
    
    def get_all(self) -> list[Product]:
        product = (self.db.query(Product)
                .options(joinedload(Product.categories))
                .all()
                )

        return product 
    
    def update(self, product_id:int, product_data:dict) -> Optional[Product]:
       
        product_update = self.get_by_id(product_id)

        if not product_update:
            return None
        
        if 'internal_code' in product_data:
            self._validate_internal_code(product_data['internal_code'], product_id)

        if 'code' in product_data:
            self._validate_code(product_data['code'], product_id)
        
        for key, value in product_data.items():
            setattr(product_update, key, value)
        self.db.commit()
        self.db.refresh(product_update)
        return product_update

    def delete(self, product_id:int) -> bool:
        product_delete = self.get_by_id(product_id)
        if product_delete:
            self.db.delete(product_delete)
            self.db.commit()
            return True
        else:
            return False
        
    def _validate_code_null(self, code: Optional[str]) -> None:
        """Valida que el código no sea nulo y no esté duplicado"""
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código del producto es obligatorio"
            )
        
    def _validate_code(self, code: Optional[str], product_id: int = None) -> None:
        """Valida que el código no esté duplicado"""
        if code:
            query = self.db.query(Product).filter(Product.code == code)
            if product_id is not None:
                query = query.filter(Product.id != product_id)
            
            if query.first() is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El código de barras ingresado para el producto ya se encuentra registrado"
                )
            
    def _validate_internal_code(self, internal_code: Optional[str], product_id: int = None) -> None:
        """Valida que el código no esté duplicado"""
        if internal_code:
            query = self.db.query(Product).filter(Product.internal_code == internal_code)
            if product_id is not None:
                query = query.filter(Product.id != product_id)
            
            if query.first() is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El código de barras ingresado para el producto ya se encuentra registrado"
                )
        
    def _generar_codigo_secuencial(self) -> str:
        """
        Genera un código secuencial de 5 dígitos basado en el último código registrado.
        Formato: 00001, 00002, ..., 99999
        """
        ultimo_codigo = self.db.query(
            func.max(Product.code)
        ).scalar() or '00000'
        
        siguiente_num = int(ultimo_codigo) + 1
        return f"{siguiente_num:05d}"  # Rellena con ceros a la izquierda
        
    #ToDo: implementar funciones para busqueda por fechas o algún otro rango