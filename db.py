import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Open .env file
# 2. Reads each line and splits on the first '=' (KEY=VALUE)
# 3. Injects those pairs into the computer's environment memory (os.environ)
load_dotenv()

# Fetch the saved secret value by its key name ('DATABASE_URL')
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set.")

# create a pipeline that connects python to postgres
engine = create_engine(DATABASE_URL)

# creates database sessions (connections) that can be used to query the database.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_session():
    """FastAPI-style dependency: yields a session, closes it after use."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()