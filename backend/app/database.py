import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database Connection URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/url_shortener"
)

# 2. SQLAlchemy Engine (Manages database connection pool)
engine = create_engine(DATABASE_URL)

# 3. SessionLocal (Factory for creating database sessions per request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base (Parent class for all our database models)
Base = declarative_base()


def get_db():
    """Dependency function to get a DB session and close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
