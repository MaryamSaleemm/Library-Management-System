"""
library_service.py

Purpose:
---------
Contains all database operations using SQLAlchemy ORM.

The CLI calls these functions instead of writing SQL queries.
"""

from datetime import date

from auth import hash_password
from database import SessionLocal
from models import Book, Loan, Member


# BOOK OPERATIONS

def add_book(title, author):

    db = SessionLocal()

    try:

        book = Book(
            title=title,
            author=author,
            available=True,
            is_deleted=False
        )

        db.add(book)
        db.commit()
        db.refresh(book)

        print("\nBook Added Successfully!")
        print(f"Book ID : {book.id}")

    finally:

        db.close()


def list_books():

    db = SessionLocal()

    try:

        books = db.query(Book).filter(
            Book.is_deleted.is_(False)
        ).all()

        if not books:

            print("\nNo Books Found.")
            return

        print("\nBOOK LIST\n")

        for book in books:

            print(
                f"ID: {book.id} | "
                f"Title: {book.title} | "
                f"Author: {book.author} | "
                f"Available: {book.available}"
            )

    finally:

        db.close()


def search_book(title):

    db = SessionLocal()

    try:

        book = db.query(Book).filter(
            Book.title == title,
            Book.is_deleted.is_(False)
        ).first()

        if book:

            print("\nBook Found\n")

            print(f"ID        : {book.id}")
            print(f"Title     : {book.title}")
            print(f"Author    : {book.author}")
            print(f"Available : {book.available}")

        else:

            print("\nBook Not Found.")

    finally:

        db.close()


def remove_book(book_id):

    db = SessionLocal()

    try:

        book = db.query(Book).filter(
            Book.id == book_id,
            Book.is_deleted.is_(False)
        ).first()

        if not book:

            print("\nBook Not Found.")
            return

        db.delete(book)

        db.commit()

        print("\nBook Deleted Successfully!")

    finally:

        db.close()


# MEMBER OPERATIONS

def register_member(name, email, phone):

    db = SessionLocal()

    try:

        username = email.split("@")[0]

        member = Member(

            name=name,
            username=username,
            email=email,
            phone=phone,
            hashed_password=hash_password("password123"),
            role="member"

        )

        db.add(member)

        db.commit()

        db.refresh(member)

        print("\nMember Registered Successfully!")
        print(f"Member ID : {member.id}")

    finally:

        db.close()


def list_members():

    db = SessionLocal()

    try:

        members = db.query(Member).all()

        print("\nMEMBERS\n")

        for member in members:

            print(

                member.id,
                member.name,
                member.username,
                member.email,
                member.phone,
                member.role

            )

    finally:

        db.close()


# LOAN OPERATIONS

def loan_book(book_id, member_id):

    db = SessionLocal()

    try:

        book = db.query(Book).filter(
            Book.id == book_id,
            Book.is_deleted.is_(False)
        ).first()

        if not book:

            print("\nBook Not Found.")
            return

        if not book.available:

            print("\nBook is already borrowed.")
            return

        member = db.query(Member).filter(
            Member.id == member_id
        ).first()

        if not member:

            print("\nMember Not Found.")
            return

        loan = Loan(

            book_id=book.id,
            member_id=member.id,
            loan_date=date.today(),
            return_date=None,
            status="borrowed"

        )

        db.add(loan)

        book.available = False

        db.commit()

        db.refresh(loan)

        print("\nBook Loaned Successfully!")
        print(f"Loan ID : {loan.id}")

    finally:

        db.close()


def return_book(book_id):

    db = SessionLocal()

    try:

        loan = db.query(Loan).filter(

            Loan.book_id == book_id,
            Loan.status == "borrowed"

        ).first()

        if not loan:

            print("\nBook is not currently borrowed.")
            return

        loan.return_date = date.today()
        loan.status = "returned"

        book = db.query(Book).filter(
            Book.id == book_id
        ).first()

        if book:

            book.available = True

        db.commit()

        print("\nBook Returned Successfully!")

    finally:

        db.close()


def list_loans():

    db = SessionLocal()

    try:

        loans = db.query(Loan).all()

        print("\nLOANS\n")

        for loan in loans:

            print(

                "Loan ID:", loan.id,
                "| Book:", loan.book.title,
                "| Member:", loan.member.name,
                "| Loan Date:", loan.loan_date,
                "| Return Date:", loan.return_date,
                "| Status:", loan.status

            )

    finally:

        db.close()