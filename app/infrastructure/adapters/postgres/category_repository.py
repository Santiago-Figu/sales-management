from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.category import Category
from app.domain.ports.category_repository import CategoryRepository
from infrastructure.database.postgres import get_db

class PostgresCategoryRepository(CategoryRepository):
    def __init__(self, db: Session):
        # super().__init__()
        self.db = db
    
    # Operaciones de CRUD básicas

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_by_id(self, category_id:int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first() 
    
    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()
    
    def update(self, category_id:int, category_data:dict) -> Optional[Category]:
        category_update = self.get_by_id(category_id)
        if category_update:
            for key, value in category_data.items():
                setattr(category_update, key, value)
            self.db.commit()
            self.db.refresh(category_update)
        else:
            #ToDo: Implementar el logger
            pass
        return category_update

    def delete(self, category_id:int) -> bool:
        category_delete = self.get_by_id(category_id)
        if category_delete:
            self.db.delete(category_delete)
            self.db.commit()
            return True
        else:
            return False
        
    #ToDo: implementar funciones para busqueda por fechas o algún otro rango