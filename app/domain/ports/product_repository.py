from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product_id: int, product_data: dict) -> Optional[Product]:
        pass

    @abstractmethod
    def delete(self, product_id:int) -> bool:
        pass