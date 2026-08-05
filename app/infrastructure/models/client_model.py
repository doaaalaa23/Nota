from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base



class ClientTable(Base):
    """
    SQLAlchemy model for Client table in the database.
    """
    __tablename__ = "clients"
    
    client_id = Column(String(14), primary_key=True, autoincrement=False)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=True)
    surety = Column(String(100), nullable=False)
    surety_num = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False )

    
    # Relationship with PhoneTable
    phone_numbers = relationship("PhoneTable", back_populates="client", cascade="all, delete-orphan")
    payings = relationship("PayingTable", back_populates="client",cascade="all, delete-orphan",overlaps="contract,payings")
    contract = relationship("ContractTable", back_populates="client", cascade="all, delete-orphan",overlaps="payings")
    users = relationship("UserTable", back_populates="clients")



    def __repr__(self):
        return (
            f"ClientTable(id={self.client_id}, name='{self.client_name}', "
            f"email='{self.client_email}', surety='{self.surety_num}', "
            f"address='{self.address}')"
        )


class PhoneTable(Base):
    """
    SQLAlchemy model for Phone table in the database.
    """
    __tablename__ = "phones"
    
    client_id = Column(String(14), ForeignKey("clients.client_id"), primary_key=True, nullable=False)
    number = Column(String(20), primary_key=True, nullable=False)
    
    # Relationship with ClientTable
    client = relationship("ClientTable", back_populates="phone_numbers")
    
    def __repr__(self):
        return f"PhoneTable(number='{self.number}', client_id={self.client_id})"
