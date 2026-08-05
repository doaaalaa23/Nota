from sqlalchemy.orm import sessionmaker, Session
from app.infrastructure.database.database import engine

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Dependency injection function for getting a database session.
    Used with FastAPI or other frameworks for automatic session management.
    
    Yields:
        SQLAlchemy Session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """
    Get a new database session.
    
    Returns:
        SQLAlchemy Session instance
    """
    return SessionLocal()
