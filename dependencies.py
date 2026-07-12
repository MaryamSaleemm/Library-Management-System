"""
dependencies.py

Contains reusable FastAPI dependencies.

"""

from database import SessionLocal


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()