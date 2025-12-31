from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy engine (connects to PostgreSQL)
db_url = settings.DATABASE_URL.replace("postgres://", "postgresql://")
engine = create_engine(db_url, echo=False)

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
