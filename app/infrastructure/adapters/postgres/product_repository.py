from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.product import Product
from domain.ports.product_repository import ProductRepository
from infrastructure.database.postgres import get_db

class PostgresProductRepository(ProductRepository):
    def __init__(self, db: Session):
        # super().__init__()
        self.db = db
    
    # Operaciones de CRUD básicas

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_by_id(self, product_id:int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self) -> list[Product]:
        return self.db.query(Product).all()
    
    def update(self, product_id:int, product_data:dict) -> Optional[Product]:
        product_update = self.get_by_id(product_id)
        if product_update:
            for key, value in product_data.items():
                setattr(product_update, key, value)
            self.db.commit()
            self.db.refresh()
        else:
            #ToDo: Implementar el logger
            pass
        return product_update

    def delete(self, product_id:int) -> bool:
        product_delete = self.get_by_id(product_id)
        if product_delete:
            self.db.delete(product_delete)
            self.db.commit()
            return True
        else:
            return False
        
    #ToDo: implementar funciones para busqueda por fechas o algún otro rango