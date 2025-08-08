from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.infrastructure.database.postgres import Base, PostgresqlDataBase

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {"schema": PostgresqlDataBase()._schema}
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=True)
    name = Column(String, nullable=False)
    contact_email = Column(String)
    contact_phone = Column(String)
    country = Column(String)
    address = Column(String)
    city = Column(String)
    zip_code = Column(String)
    company_name = Column(String) # razón social
    rfc = Column(String)

    # products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier {self.name}>"

Supplier.__table__