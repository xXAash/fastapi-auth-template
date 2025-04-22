from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL - change later if you move to PostgreSQL/MySQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./auth.db"

# Connects to SQLite (check_same_thread is needed for SQLite only)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class to interact with DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to define models (tables)
Base = declarative_base()