from typing import List, Optional
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.domain.models.base import Base
from app.core.settings.configdb import settings

class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA, "extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    # prefix: Mapped[str] = mapped_column(String(3), nullable=False, default='N/A')

    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        default=func.now()
    )

    last_update: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        default=func.now()
    )

    # Relationship

    # Tipo: Uno a Muchos
    # Muchos productos tienen una categoria

    products: Mapped[List["app.domain.models.product.Product"]] = relationship(
        "app.domain.models.product.Product", 
        back_populates="categories",
        # cascade="all, delete-orphan" # para borrado en cascada si es necesario
    )


    def __repr__(self):
        return f"<Category {self.name}>"
    

Category.__table__