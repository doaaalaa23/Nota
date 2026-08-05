from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from datetime import datetime
from app.infrastructure.database.base import Base 
from sqlalchemy.orm import relationship


class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    google_sub = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    user_name = Column(String, nullable=False)
    picture_url = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)


    clients = relationship("ClientTable", back_populates="users", cascade="all, delete-orphan")
    products = relationship("ProductTable", back_populates="users", cascade="all, delete-orphan")
    contracts = relationship("ContractTable", back_populates="users", cascade="all, delete-orphan")
    payings = relationship("PayingTable", back_populates="users", cascade="all, delete-orphan")



