from typing import TypedDict
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.postgres import Base, PostgresqlDataBase

class Product(Base):
    """
    Representación del objeto producto para almacenamiento en base de datos.
    """
    __tablename__ = "products"
    __table_args__ = {"schema": PostgresqlDataBase()._schema}
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    # supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    # supplier = relationship("Supplier", back_populates="products")
    # costs = relationship("ProductCost", back_populates="product")
    # sale_items = relationship("SaleItem", back_populates="product")

    def __repr__(self):
        """
        Permite visualizar los datos del objeto seleccionado sin acceder directamente a sus propiedades.
        """
        return f"<Product {self.name}>"

Product.__table__ 