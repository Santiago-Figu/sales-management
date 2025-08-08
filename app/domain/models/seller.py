from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.postgres import Base, PostgresqlDataBase

class Seller(Base):
    """
    Representación del objeto vendedor para almacenamiento en base de datos.
    """
    __tablename__ = "sellers"
    __table_args__ = {"schema": PostgresqlDataBase()._schema}
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String,nullable=False, unique=True)
    phone = Column(String)
    

    # sales = relationship("Sale", back_populates="seller")

    def __repr__(self):
        return f"<Seller {self.name}>"
    
Seller.__table__ 