from typing import Optional
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.domain.models.base import Base
from app.core.settings.configdb import settings

class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA, "extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3), default='MXN')
    internal_code: Mapped[str] = mapped_column(String(5), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=True)
    stock: Mapped[int] = mapped_column(Integer,default=0)
    stock_min: Mapped[int] = mapped_column(Integer,default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

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
    
    # Foreign Key
    # productos -> categoría
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.category.id",
            ondelete="SET NULL" # para volver nulo en caso de borrado
        ),
        nullable=True # permite nulos para el caso en el que se borre una categoria
    )
    
    # Relationship
    # Tipo: Muchos a uno
    # muchos productos tienen una categoría
    categories: Mapped["app.domain.models.category.Category"] = relationship("app.domain.models.category.Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product {self.name}>"

Product.__table__