from typing import Optional
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.domain.models.base import Base
from app.core.settings.configdb import settings

class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA, "extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    hiring_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    salary: Mapped[float] = mapped_column(DECIMAL(15,2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='MXN')
    active: Mapped[bool] = mapped_column(Boolean,nullable=False, default=True)
    is_system_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)    

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
    )

    # Todo: falta la relación con roles

    def __repr__(self):
        return f"<Product {self.name}>"

Employee.__table__