from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: int, user_data: dict) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user:int) -> bool:
        pass