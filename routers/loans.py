from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from dependencies import get_db

from fastapi import BackgroundTasks
from services.notification_service import send_borrow_notification
from auth import (
    get_current_user,
    get_current_librarian
)

from models import (
    Book,
    Loan,
    Member
)

from schemas import (   # how the API response should look
    LoanResponse,
    LoanDetailResponse
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)

# BORROW BOOK

@router.post(
    "/borrow/{book_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Borrow Book",
    description="Borrow an available book."
)
def borrow_book(
    book_id: int,                       # Reads /borrow/5 and stores book_id = 5
    background_tasks: BackgroundTasks,  # FastAPI automatically creates one BackgroundTask object.
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    # CHECK WHETHER BOOK EXISTS

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    # CHECK SOFT DELETE

    if book.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )

    # CHECK BOOK AVAILABILITY

    if not book.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is currently unavailable."
        )

    # MAXIMUM 3 ACTIVE LOANS

    active_loans = db.query(Loan).filter(
        Loan.member_id == current_user.id,
        Loan.status == "borrowed"
    ).count()

    if active_loans >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have reached the maximum borrowing limit (3 books)."
        )

    # PREVENT DUPLICATE BORROW

    existing_loan = db.query(Loan).filter(
        Loan.book_id == book.id,
        Loan.member_id == current_user.id,
        Loan.status == "borrowed"
    ).first()

    if existing_loan:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already borrowed this book."
        )

    # CREATE LOAN

    new_loan = Loan(
        book_id=book.id,
        member_id=current_user.id,
        loan_date=date.today(),
        status="borrowed"
    )

    # UPDATE BOOK STATUS

    book.available = False

    db.add(new_loan)    # Places object inside SQLAlchemy Session

    db.commit()

    db.refresh(new_loan)

    background_tasks.add_task( # run after response to user
        send_borrow_notification,
        current_user.username,
        book.title
    )

    

    return new_loan


# RETURN BOOK

@router.post(
    "/return/{loan_id}",
    response_model=LoanResponse,
    summary="Return Book"
)
def return_book(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    loan = db.query(Loan).filter(
        Loan.id == loan_id
    ).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found."
        )

    if (
        current_user.role != "librarian"
        and loan.member_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed."
        )

    if loan.status == "returned":
        raise HTTPException(
            status_code=400,
            detail="Book already returned."
        )

    loan.status = "returned"
    loan.return_date = date.today()

    book = db.query(Book).filter(
        Book.id == loan.book_id
    ).first()

    if book:
        book.available = True

    db.commit()

    db.refresh(loan)

    return loan


# MY LOANS

@router.get(
    "/me",
    response_model=list[LoanDetailResponse],
    summary="My Loans"
)
def my_loans(
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    loans = db.query(Loan).filter(
        Loan.member_id == current_user.id
    ).all()

    return loans


# VIEW ALL LOANS (LIBRARIAN)

@router.get(
    "/",
    response_model=list[LoanDetailResponse],
    summary="View All Loans"
)
def all_loans(
    db: Session = Depends(get_db),
    librarian: Member = Depends(get_current_librarian)
):

    loans = db.query(Loan).all()

    return loans