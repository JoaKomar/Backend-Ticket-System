from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import DATABASE_URL as db

# PostgreSQL Configuration
DATABASE_URL = db

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


#To KEEP open the Session with DB
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


