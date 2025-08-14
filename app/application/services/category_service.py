from typing import List, Optional
from app.domain.models.category import Category
from app.application.use_cases.category_use_cases import CategoryUseCases
from app.infrastructure.adapters.postgres.category_repository import PostgresCategoryRepository
from app.infrastructure.database.postgres import get_db

class CategoryService:
    
    @staticmethod
    def create_category(category_data: dict) -> Category:
        print("1")
        db = next(get_db())
        repo = PostgresCategoryRepository(db)
        use_cases = CategoryUseCases(repo)
        return use_cases.create_category(category_data)
    
    @staticmethod
    def get_category(category_id: int) -> Optional[Category]:
        db = next(get_db())
        repo = PostgresCategoryRepository(db)
        use_cases = CategoryUseCases(repo)
        return use_cases.get_category(category_id)
    
    @staticmethod
    def get_all_categories() -> List[Category]:
        db = next(get_db())
        repo = PostgresCategoryRepository(db)
        use_cases = CategoryUseCases(repo)
        return use_cases.get_all_categorys()
    
    @staticmethod
    def update_category(category_id: int, category_data: dict) -> Optional[Category]:
        db = next(get_db())
        repo = PostgresCategoryRepository(db)
        use_cases = CategoryUseCases(repo)
        return use_cases.update_category(category_id, category_data)
    
    @staticmethod
    def delete_category(category_id: int) -> bool:
        db = next(get_db())
        repo = PostgresCategoryRepository(db)
        use_case = CategoryUseCases(repo)
        return use_case.delete_category(category_id)