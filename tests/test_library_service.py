import uuid

from database import SessionLocal
from library_service import (
    add_book,
    register_member,
    loan_book,
    return_book,
)

from models import Book
from models import Member
from models import Loan


def test_add_book():

    title = f"Test Book {uuid.uuid4()}"
    author = "Test Author"

    add_book(title, author)

    db = SessionLocal()

    try:

        book = db.query(Book).filter(Book.title == title).first()

        assert book is not None
        assert book.author == author
        assert book.available is True

    finally:

        db.close()


def test_register_member():

    email = f"{uuid.uuid4()}@example.com"

    register_member(
        "Test User",
        email,
        "03001234567"
    )

    db = SessionLocal()

    try:

        member = db.query(Member).filter(Member.email == email).first()

        assert member is not None
        assert member.name == "Test User"

    finally:

        db.close()


def test_loan_and_return_book():

    db = SessionLocal()

    try:

        title = f"Loan Book {uuid.uuid4()}"

        book = Book(
            title=title,
            author="Tester",
            available=True
        )

        member = Member(
            name="Loan User",
            email=f"{uuid.uuid4()}@example.com",
            phone="03111111111"
        )

        db.add(book)
        db.add(member)

        db.commit()

        db.refresh(book)
        db.refresh(member)

        book_id = book.id
        member_id = member.id

    finally:

        db.close()

    loan_book(book_id, member_id)

    db = SessionLocal()

    try:

        loan = db.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.status == "Borrowed"
        ).first()

        assert loan is not None

        book = db.query(Book).filter(Book.id == book_id).first()

        assert book.available is False

    finally:

        db.close()

    return_book(book_id)

    db = SessionLocal()

    try:

        loan = db.query(Loan).filter(
            Loan.book_id == book_id
        ).first()

        assert loan.status == "Returned"

        book = db.query(Book).filter(Book.id == book_id).first()

        assert book.available is True

    finally:

        db.close()
