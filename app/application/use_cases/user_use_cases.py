from typing import List, Optional
from app.domain.models.user import User
from app.domain.ports.user_repository import UserRepository


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        return self.repository.create(user)
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        return self.repository.get_all()
    
    def update_user(self, user_id:int, user_data: dict) -> Optional[User]:
        return self.repository.update(user_id,user_data)
    
    def delete_user(self, user_id:int) -> bool:
        return self.repository.delete(user_id)