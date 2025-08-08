from typing import List, Optional
from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository

print(f"Definiendo modelo Product (ejecutado desde: {__file__})")

class ProductUseCases:
    def __init__(self, product_repository: ProductRepository):
        self.repository = product_repository

    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        return self.repository.create(product)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id)
    
    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()
    
    def update_product(self, product_id:int, product_data: dict) -> Optional[Product]:
        return self.repository.update(product_id,product_data)
    
    def delete_product(self, product_id:int) -> bool:
        return self.repository.delete(product_id)