from typing import List, Optional
from app.domain.models.user import User
from app.application.use_cases.user_use_cases import UserUseCases
from app.infrastructure.adapters.postgres.user_repository import PostgresUserRepository
from app.infrastructure.database.postgres import get_db

class UserService:
    
    @staticmethod
    def create_user(user_data: dict) -> User:
        db = next(get_db())
        repo = PostgresUserRepository(db)
        use_cases = UserUseCases(repo)
        return use_cases.create_user(user_data)
    
    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        db = next(get_db())
        repo = PostgresUserRepository(db)
        use_cases = UserUseCases(repo)
        return use_cases.get_user(user_id)
    
    @staticmethod
    def get_all_users() -> List[User]:
        db = next(get_db())
        repo = PostgresUserRepository(db)
        use_cases = UserUseCases(repo)
        return use_cases.get_all_users()
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> Optional[User]:
        db = next(get_db())
        repo = PostgresUserRepository(db)
        use_cases = UserUseCases(repo)
        return use_cases.update_user(user_id, user_data)
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        db = next(get_db())
        repo = PostgresUserRepository(db)
        use_case = UserUseCases(repo)
        return use_case.delete_user(user_id)