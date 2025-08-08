# app/domain/models/__init__.py
from app.infrastructure.database.postgres import Base
from .product import Product
from .supplier import Supplier
from .seller import Seller

# Fuerza el registro de modelos
__all__ = ['Product', 'Supplier', 'Seller']