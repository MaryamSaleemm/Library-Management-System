from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from dependencies import get_db

from models import Member

from schemas import (
    MemberCreate,
    MemberResponse,
    Token,
)

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# SIGNUP

@router.post(
    "/signup",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    member: MemberCreate,
    db: Session = Depends(get_db)
):

    existing_username = db.query(Member).filter(
        Member.username == member.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )

    existing_email = db.query(Member).filter(
        Member.email == member.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    new_member = Member(
        name=member.name,
        username=member.username,
        email=member.email,
        phone=member.phone,
        hashed_password=hash_password(member.password),
        role="member"
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# LOGIN

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(Member).filter(
        Member.username == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# CURRENT USER

@router.get(
    "/me",
    response_model=MemberResponse
)
def get_profile(
    current_user: Member = Depends(get_current_user)
):

    return current_user