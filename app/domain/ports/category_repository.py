from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.category import Category

class CategoryRepository(ABC):
    
    @abstractmethod
    def create(self,category: Category) -> Category:
        print("3")
        # pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all(self) -> List[Category]:
        pass

    @abstractmethod
    def update(self, category_id: int, product_data: dict) -> Optional[Category]:
        pass

    @abstractmethod
    def delete(self, category_id:int) -> bool:
        pass