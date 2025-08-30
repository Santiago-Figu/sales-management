from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.domain.models.base import Base
from app.core.settings.configdb import settings

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": settings.POSTGRES_SCHEMA, "extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str]  = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str]  = mapped_column(String(150), nullable=False)
    email: Mapped[str]  = mapped_column(String(150), unique=True, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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

    def __repr__(self):
        return f"<Data User: {self.first_name} {self.last_name}>"

User.__table__
