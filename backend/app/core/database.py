from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

#SQLite needs this flag becaue FastAPI uses several threads
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

#  pool_pre_ping check is there any active connection
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase): #Base class for all models to inherit from
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()