from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Sqlalchemy database engine
engine = create_engine(settings.P_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create database session
def get_db_session():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
