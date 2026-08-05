from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class PayingTable(Base):
    __tablename__ = "payings"

    paying_id = Column(Integer, primary_key=True, autoincrement=True)
    paid_amount = Column(Float, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False)
    client_id = Column(String(14), ForeignKey("clients.client_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    paying_date = Column(Date, nullable=False)
    notice = Column(String(300), nullable=True)
# Relationship with ClientTable
    client = relationship("ClientTable", back_populates="payings",overlaps="contract,payings")
# Relationship with ContractTableTable
    contract = relationship("ContractTable", back_populates="payings",overlaps="payings")
    users = relationship("UserTable", back_populates="payings")

    