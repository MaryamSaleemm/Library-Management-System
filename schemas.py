from datetime import date

from pydantic import BaseModel, EmailStr, Field


# BOOK SCHEMAS

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    available: bool = True


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    available: bool | None = None  # = None means default value can be none


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    available: bool
    is_deleted: bool

    class Config:   # pydantic expect dictionary not an SQLAlchemy object which we are giving so we let the pydantic to read the object's attibute value and later it convert to json and return
        from_attributes = True


# MEMBER SCHEMAS

class MemberCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=6)


class MemberResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str | None
    role: str

    class Config:
        from_attributes = True


# TOKEN SCHEMAS

class Token(BaseModel):
    access_token: str
    token_type: str


# LOAN SCHEMAS

class LoanResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    loan_date: date
    return_date: date | None
    status: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):
    id: int
    loan_date: date
    return_date: date | None
    status: str

    book: BookResponse
    member: MemberResponse

    class Config:
        from_attributes = True