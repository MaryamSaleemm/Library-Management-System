"""
database.py

Purpose:
---------
This file is responsible for configuring SQLAlchemy.

It performs the following tasks:
1. Loads environment variables from the .env file.
2. Creates the database connection URL.
3. Creates the SQLAlchemy Engine.
4. Creates Session objects for database operations.
5. Creates the Base class that all ORM models will inherit from.
"""

            # Tells How do we connect to PostgreSQL?

import os

from dotenv import load_dotenv

from sqlalchemy import create_engine             #It manages the connection to PostgreSQL from the APP
from sqlalchemy.orm import declarative_base      # create the Base class that all ORM models will inherit from / Python class is actually a database table
from sqlalchemy.orm import sessionmaker         #it performs the database operations (i.e crud) 


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# SQLAlchemy Database URL
# Format: postgresql+psycopg2://username:password@host:port/database

DATABASE_URL = (
    f"postgresql+psycopg2://"          #Use PostgreSQL as the database & Use the psycopg2 driver to communicate with PostgreSQL
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

 
# Create SQLAlchemy Engine
# The Engine manages the connection to PostgreSQL it does not immediately build the connection, instead it prepares the conn for future use if the user want to excess the db then it will build the conn.

engine = create_engine(
    DATABASE_URL,
    echo=True           # Prints SQL queries in the terminal (useful while learning when any of our fun is not working properly)
)

# Create Session Factory
# Every database operation will use a Session object.

SessionLocal = sessionmaker(
    bind=engine,    #There could be many dbs,bind=engine means Whenever you create a Session, use THIS Engine.
    autoflush=False,    #not to Send pending changes to PostgreSQL until flush().
    autocommit=False       #Alchemy should not save things auto until ypu write db.commit() for it to save
)

# Base Class
# All ORM models (Book, Member, Loan)
# will inherit from this Base class.

Base = declarative_base()