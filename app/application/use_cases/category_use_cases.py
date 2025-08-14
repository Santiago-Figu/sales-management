from typing import List, Optional
from app.domain.models.category import Category
from app.domain.ports.category_repository import CategoryRepository

# print(f"Definiendo modelo category (ejecutado desde: {__file__})")

class CategoryUseCases:
    def __init__(self, category_repository: CategoryRepository):
        self.repository = category_repository

    def create_category(self, category_data: dict) -> Category:
        print("2")
        category = Category(**category_data)
        print("2.1")
        return self.repository.create(category)
    
    def get_category(self, category_id: int) -> Optional[Category]:
        return self.repository.get_by_id(category_id)
    
    def get_all_categorys(self) -> List[Category]:
        return self.repository.get_all()
    
    def update_category(self, category_id:int, category_data: dict) -> Optional[Category]:
        return self.repository.update(category_id,category_data)
    
    def delete_category(self, category_id:int) -> bool:
        return self.repository.delete(category_id)