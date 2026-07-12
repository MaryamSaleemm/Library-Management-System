"""
models.py

Purpose:
---------
This file contains all the database tables of the Library
Management System.

Each Python class represents one table in PostgreSQL.

Tables:
1. Books
2. Members
3. Loans
"""
# What tables should PostgreSQL have

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# BOOK TABLE


class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    author = Column(String, nullable=False)

    available = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean, nullable=False, default=False)   
    
    loans = relationship("Loan", back_populates="book")  


# MEMBER TABLE


class Member(Base):

    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    # Username used during login
    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    phone = Column(String)

    # Never store plain passwords
    # We will store a bcrypt hash here
    hashed_password = Column(String, nullable=False)

    # Determines what the user is allowed to do
    role = Column(String, nullable=False, default="member")

    # Relationship with loans
    loans = relationship("Loan", back_populates="member")  #member.loans
    
# LOAN TABLE


class Loan(Base):

    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    book_id = Column(Integer, ForeignKey("books.id"))

    member_id = Column(Integer, ForeignKey("members.id"))

    loan_date = Column(Date)

    return_date = Column(Date)

    status = Column(String)

    book = relationship("Book", back_populates="loans")

    member = relationship("Member", back_populates="loans")

    # relationship() creates Python objects without sql query,joins
