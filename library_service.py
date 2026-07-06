"""
library_service.py

Purpose:
---------
Contains all database operations using SQLAlchemy ORM.

The CLI calls these functions instead of writing SQL queries.

Operations:
1. Add Book
2. List Books
3. Search Book
4. Remove Book
5. Register Member
6. Loan Book
7. Return Book
"""

from datetime import date
from database import SessionLocal

from models import Book
from models import Member
from models import Loan


# BOOK OPERATIONS

def add_book(title, author):

    db = SessionLocal()                 #SQLAlchemy creates a new database session,Every function opens its own session.

    try:

        book = Book(                    #It simply creates a Python object,It only exists in memory.
            title=title,
            author=author,
            available=True
        )

        db.add(book)                    # Want to insert this object into the database, still postgre has not executed any sql query yet

        db.commit()                     #Now SQLAlchemy sends SQL to PostgreSQL.

        print("\nBook Added Successfully!")
        print(f"Book ID : {book.id}")

    finally:

        db.close()                  #session closed



def list_books():

    db = SessionLocal()

    try:

        books = db.query(Book).all()

        if not books:

            print("\nNo Books Found.")
            return

        print("\n BOOK LIST \n")

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

        book = db.query(Book).filter(Book.title == title).first()

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

        book = db.query(Book).filter(Book.id == book_id).first()

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

        member = Member(

            name=name,

            email=email,

            phone=phone

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

    members = db.query(Member).all()

    print("\nMembers\n")

    for member in members:

        print(
            member.id,
            member.name,
            member.email,
            member.phone
        )

    db.close()



# LOAN OPERATIONS

def loan_book(book_id, member_id):

    db = SessionLocal()

    try:

        # Find the book
        book = db.query(Book).filter(Book.id == book_id).first()

        if not book:

            print("\nBook Not Found.")
            return

        # Check availability
        if not book.available:

            print("\nBook is already loaned.")
            return

        # Find member
        member = db.query(Member).filter(Member.id == member_id).first()

        if not member:

            print("\nMember Not Found.")
            return

        # Create loan record
        loan = Loan(

            book_id=book.id,

            member_id=member.id,

            loan_date=date.today(),

            return_date=None,

            status="Borrowed"

        )

        db.add(loan)

        # Mark book unavailable
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

        # Find active loan
        loan = db.query(Loan).filter(

            Loan.book_id == book_id,

            Loan.status == "Borrowed"

        ).first()

        if not loan:

            print("\nThis book is not currently loaned.")
            return

        # Update loan
        loan.return_date = date.today()

        loan.status = "Returned"

        # Make book 
        # available again
        book = db.query(Book).filter(Book.id == book_id).first()

        if book:

            book.available = True

        db.commit()

        print("\nBook Returned Successfully!")

    finally:

        db.close()
        
        
def list_loans():

    db = SessionLocal()

    loans = db.query(Loan).all()

    print("\nLoans\n")

    for loan in loans:

        print(

            "Loan ID:", loan.id,

            "| Book:", loan.book.title,

            "| Member:", loan.member.name,

            "| Loan Date:", loan.loan_date,

            "| Return Date:", loan.return_date,

            "| Status:", loan.status

        )

    db.close()