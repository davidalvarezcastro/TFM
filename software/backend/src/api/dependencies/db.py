""" Database session dependencies """
from src.database.mysql import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
