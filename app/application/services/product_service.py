from typing import List, Optional
from app.domain.models.product import Product
from app.application.use_cases.product_use_cases import ProductUseCases
from app.infrastructure.adapters.postgres.product_repository import PostgresProductRepository
from app.infrastructure.database.postgres import get_db

class ProductService:
    
    @staticmethod
    def create_product(product_data: dict) -> Product:
        db = next(get_db())
        repo = PostgresProductRepository(db)
        use_cases = ProductUseCases(repo)
        return use_cases.create_product(product_data)
    
    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        db = next(get_db())
        repo = PostgresProductRepository(db)
        use_cases = ProductUseCases(repo)
        return use_cases.get_product(product_id)
    
    @staticmethod
    def get_all_products() -> List[Product]:
        db = next(get_db())
        repo = PostgresProductRepository(db)
        use_cases = ProductUseCases(repo)
        return use_cases.get_all_products()
    
    @staticmethod
    def update_product(product_id: int, product_data: dict) -> Optional[Product]:
        db = next(get_db())
        repo = PostgresProductRepository(db)
        use_cases = ProductUseCases(repo)
        return use_cases.update_product(product_id, product_data)
    
    @staticmethod
    def delete_product(product_id: int) -> bool:
        db = next(get_db())
        repo = PostgresProductRepository(db)
        use_case = ProductUseCases(repo)
        return use_case.delete_product(product_id)