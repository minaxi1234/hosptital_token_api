from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy engine (connects to PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # set to True only for debugging SQL queries
)

# Session Local class for DB sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency for FastAPI (we will use this in routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
