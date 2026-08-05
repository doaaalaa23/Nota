import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

# Database connection URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing DATABASE_URL environment variable.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=True  # Set to False in production
)


def init_db():
    """
    Initialize the database by creating all tables.
    """
    from app.infrastructure.models.client_model import Base as ClientBase
    from app.infrastructure.models.product_model import Base as ProductBase
    from app.infrastructure.models.contract_model import Base as ContractBase
    from app.infrastructure.models.paying_model import Base as PayingBase
    from app.infrastructure.models.user_model import Base as UserBase

    ClientBase.metadata.create_all(bind=engine)
    ProductBase.metadata.create_all(bind=engine)
    ContractBase.metadata.create_all(bind=engine)
    PayingBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
   

def get_engine():
    """
    Get the SQLAlchemy engine instance.
    
    Returns:
        SQLAlchemy Engine
    """
    return engine
