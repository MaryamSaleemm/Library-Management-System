import os

# These are used for token expiration.
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from dotenv import load_dotenv

# This library creates and verifies JWTs.
from jose import JWTError
from jose import jwt

from passlib.context import CryptContext  # Used for password hashing

from fastapi import Depends # Dependency Injection
from fastapi import HTTPException # Allows returning proper HTTP errors
from fastapi import status

from fastapi.security import OAuth2PasswordBearer # this create authorize button inside swagger

from dependencies import get_db
from sqlalchemy.orm import Session
from models import Member

load_dotenv()

# JWT Configuration

SECRET_KEY = os.getenv("SECRET_KEY")  #  a private key used to sign and verify JWT tokens

ALGORITHM = "HS256" #  a standard symmetric-key JWT signing method.

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2

oauth2_scheme = OAuth2PasswordBearer(       # "Protected endpoints should expect a Bearer token in the Authorization header."
    tokenUrl="/users/login"                 # Which endpoint generates the token?
)

# Password Hashing

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"  # If an old password hash is detected,automatically treat it as outdated.
)


def hash_password(password: str): # signup call this and the password is hashed and the db stores hashed password

    return pwd_context.hash(password)


def verify_password(  # after the user signup , login use this method, bycrypt hash it and the password that stores in db during signup and verify as they Are same or not and return T/F
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# JWT

def create_access_token(data: dict): # Called after successful login

    to_encode = data.copy()          # copies the dic never modify the original

    expire = datetime.now(
        timezone.utc
    ) + timedelta(              # add time after which token expires 
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(       # adds expiration time to the dic
        {
            "exp": expire
        }
    )

    return jwt.encode(      # convert dic to jwt and return it to the user
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            return None

        return username

    except JWTError:

        return None

# Logged-in User

def get_current_user(

    token: str = Depends(oauth2_scheme), # FastAPI automatically reads the token from the request header.

    db: Session = Depends(get_db)

):

    username = verify_access_token(token)

    if username is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(Member).filter(
        Member.username == username
    ).first()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Librarian Authorization

def get_current_librarian(

    current_user: Member = Depends(  # this authenticate only then check role
        get_current_user
    )

):

    if current_user.role.lower() != "librarian":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only librarians can perform this action."
        )

    return current_user