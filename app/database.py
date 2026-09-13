from sqlalchemy import create_engine
from app.models import Base,users
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("Database Connected!")

Base.metadata.create_all(engine)

SessionLocal=sessionmaker(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

