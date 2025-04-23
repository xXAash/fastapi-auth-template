import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Load the database URL from the environment or use SQLite as the default
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

# Create the database engine
# For SQLite, we use `check_same_thread=False` to allow multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining ORM models
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session.
    Yields a database session for the request lifecycle.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()