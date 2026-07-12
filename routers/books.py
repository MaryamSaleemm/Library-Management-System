from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from dependencies import get_db

from auth import (
    get_current_user,
    get_current_librarian
)

from models import Book
from models import Member

from schemas import (
    BookCreate,
    BookUpdate,
    BookResponse
)

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# GET ALL AVAILABLE BOOKS

@router.get(
    "/",
    response_model=list[BookResponse],
    summary="View Available Books",
    description="Returns all books that are available and not deleted."
)
def get_books(
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    books = (
        db.query(Book)
        .filter(
            Book.available == True,
            Book.is_deleted == False
        )
        .all()
    )

    return books

# GET BOOK BY ID

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get Book by ID"
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    return book

# SEARCH BOOK

@router.get(
    "/search/",
    response_model=list[BookResponse],
    summary="Search Books"
)
def search_books(
    title: str,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    books = (
        db.query(Book)
        .filter(
            Book.title.ilike(f"%{title}%"),
            Book.available == True,
            Book.is_deleted == False
        )
        .all()
    )

    return books

# ADD BOOK

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Book"
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    librarian: Member = Depends(get_current_librarian)
):

    existing = (
        db.query(Book)
        .filter(
            Book.title == book.title,
            Book.author == book.author,
            Book.is_deleted == False
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists."
        )

    new_book = Book(
        title=book.title,
        author=book.author,
        available=book.available
    )

    db.add(new_book)

    db.commit()

    db.refresh(new_book)

    return new_book


# UPDATE BOOK

@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update Book"
)
def update_book(
    book_id: int,
    updated_book: BookUpdate,
    db: Session = Depends(get_db),
    librarian: Member = Depends(get_current_librarian)
):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    update_data = updated_book.model_dump(exclude_unset=True)

    for key, value in update_data.items():

        setattr(book, key, value)

    db.commit()

    db.refresh(book)

    return book

# SOFT DELETE BOOK

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Book"
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    librarian: Member = Depends(get_current_librarian)
):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    if not book.available:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a borrowed book."
        )

    book.is_deleted = True

    db.commit()

    return {
        "message": "Book deleted successfully."
    }