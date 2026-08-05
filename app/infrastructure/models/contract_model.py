from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class ContractTable(Base):
    """SQLAlchemy model for Contract table in the database."""
    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer,ForeignKey("products.product_id"),nullable=False )
    client_id = Column(String(14), ForeignKey("clients.client_id"),nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    sale_date = Column(Date, nullable=False)
    sale_price = Column(Float, nullable=False)
    receiving_price = Column(Float, nullable=False)
    remaining_price = Column(Float, nullable=False)
    installment_value = Column(Float, nullable=False)
    installment_num = Column(Integer, nullable=False)
    paying_day = Column(Integer, nullable=False)
    first_installment = Column(Date, nullable=False)

    payings = relationship("PayingTable", back_populates="contract", cascade="all, delete-orphan",overlaps="client,payings")
    client = relationship("ClientTable", back_populates="contract")
    product = relationship("ProductTable", back_populates="contract")
    users = relationship("UserTable", back_populates="contracts")


