"""
seed.py

Purpose:
---------
Insert initial (seed) data into the database.

This script:
1. Creates default books.
2. Creates default members.
3. Prevents duplicate data.
"""

from sqlalchemy.orm import Session

from database import SessionLocal
from models import Book
from models import Member


def seed_database():

    db: Session = SessionLocal()

    try:

        # Seed Books

        if db.query(Book).count() == 0:

            books = [

                Book(
                    title="Python Programming",
                    author="John Smith",
                    available=True
                ),

                Book(
                    title="Docker Essentials",
                    author="Alice Brown",
                    available=True
                ),

                Book(
                    title="PostgreSQL Basics",
                    author="David Wilson",
                    available=True
                )

            ]

            db.add_all(books)

            print("Books seeded.")

        else:

            print("Books already exist. Skipping...")

        # Seed Members

        if db.query(Member).count() == 0:

            members = [

                Member(
                    name="Maryam",
                    email="maryam@example.com",
                    phone="03001234567"
                ),

                Member(
                    name="Ali",
                    email="ali@example.com",
                    phone="03111234567"
                )

            ]

            db.add_all(members)

            print("Members seeded.")

        else:

            print("Members already exist. Skipping...")

        db.commit()

        print("\nDatabase seeded successfully!")

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()