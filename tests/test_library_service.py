"""
tests/test_library_service.py

Integration Tests
-----------------
Tests the real Library Management System against PostgreSQL.

Requirements:
- PostgreSQL running
- Alembic migrations applied
"""

import uuid

from database import SessionLocal

from models import Book
from models import Member
from models import Loan
from auth import hash_password

from library_service import (
    add_book,
    search_book,
    remove_book,
    register_member,
    loan_book,
    return_book,
)

# ADD BOOK

def test_add_book():

    title = f"Book-{uuid.uuid4()}"

    add_book(
        title,
        "Test Author"
    )

    db = SessionLocal()

    book = db.query(Book).filter(
        Book.title == title
    ).first()

    assert book is not None
    assert book.author == "Test Author"
    assert book.available is True

    db.delete(book)
    db.commit()
    db.close()


# SEARCH BOOK


def test_search_book(capsys):

    title = f"Book-{uuid.uuid4()}"

    add_book(title, "John Smith")

    search_book(title)

    captured = capsys.readouterr()

    assert title in captured.out

# REMOVE BOOK


def test_remove_book():

    db = SessionLocal()

    book = Book(

        title=f"Delete-{uuid.uuid4()}",

        author="Delete Author",

        available=True

    )

    db.add(book)

    db.commit()

    db.refresh(book)

    book_id = book.id

    db.close()

    remove_book(book_id)

    db = SessionLocal()

    deleted = db.query(Book).filter(

        Book.id == book_id

    ).first()

    assert deleted is None

    db.close()


# REGISTER MEMBER


def test_register_member():

    email = f"{uuid.uuid4()}@example.com"

    register_member(

        "PyTest User",

        email,

        "03001234567"

    )

    db = SessionLocal()

    member = db.query(Member).filter(

        Member.email == email

    ).first()

    assert member is not None

    assert member.name == "PyTest User"

    db.delete(member)

    db.commit()

    db.close()


# LOAN BOOK


def test_loan_book():

    db = SessionLocal()

    book = Book(

        title=f"Loan-{uuid.uuid4()}",

        author="Loan Author",

        available=True

    )

    member = Member(
    name="Loan Member",
    username=f"user_{uuid.uuid4().hex[:8]}",
    email=f"{uuid.uuid4()}@example.com",
    phone="03000000000",
    hashed_password=hash_password("password123"),
    role="member"
)

    db.add(book)

    db.add(member)

    db.commit()

    db.refresh(book)

    db.refresh(member)

    book_id = book.id

    member_id = member.id

    db.close()

    loan_book(

        book_id,

        member_id

    )

    db = SessionLocal()

    loan = db.query(Loan).filter(

        Loan.book_id == book_id

    ).first()

    assert loan is not None

    assert loan.status == "borrowed"

    updated_book = db.query(Book).filter(

        Book.id == book_id

    ).first()

    assert updated_book.available is False

    db.close()


# RETURN BOOK

def test_return_book():

    db = SessionLocal()

    book = Book(

        title=f"Return-{uuid.uuid4()}",

        author="Return Author",

        available=True

    )

    member = Member(
    name="Return Member",
    username=f"user_{uuid.uuid4().hex[:8]}",
    email=f"{uuid.uuid4()}@example.com",
    phone="03110000000",
    hashed_password=hash_password("password123"),
    role="member"
)

    db.add(book)

    db.add(member)

    db.commit()

    db.refresh(book)

    db.refresh(member)

    loan = Loan(

        book_id=book.id,

        member_id=member.id,

        status="borrowed"

    )

    book.available = False

    db.add(loan)

    db.commit()

    book_id = book.id

    db.close()

    return_book(book_id)

    db = SessionLocal()

    updated_loan = db.query(Loan).filter(

        Loan.book_id == book_id

    ).first()

    updated_book = db.query(Book).filter(

        Book.id == book_id

    ).first()

    assert updated_loan.status == "returned"

    assert updated_loan.return_date is not None

    assert updated_book.available is True

    db.delete(updated_loan)

    db.delete(updated_book)

    member = db.query(Member).filter(

        Member.email.like("%@example.com")

    ).filter(

        Member.name == "Return Member"

    ).first()

    if member:

        db.delete(member)

    db.commit()

    db.close()