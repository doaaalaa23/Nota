from sqlalchemy import Column, ForeignKey, Integer, String, Float
from app.infrastructure.database.base import Base
from sqlalchemy.orm import relationship

class ProductTable(Base):
    """
    SQLAlchemy model for Product table in the database.
    """
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    product_price = Column(Float, nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False )

    
    contract = relationship("ContractTable", back_populates="product")
    users = relationship("UserTable", back_populates="products")


    