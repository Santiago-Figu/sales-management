from typing import List, Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.models.base import Base
from app.core.settings.configdb import settings
class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA, "extend_existing": True}
    # __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    # active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationship

    # Tipo: Uno a Muchos
    # Muchos productos tienen una categoria

    products: Mapped[List["app.domain.models.product.Product"]] = relationship(
        "app.domain.models.product.Product", 
        back_populates="categories",
        # cascade="all, delete-orphan" # para borrado en cascada
    )


    def __repr__(self):
        return f"<Category {self.name}>"
    

Category.__table__