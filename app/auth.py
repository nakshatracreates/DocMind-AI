import bcrypt
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import users
from app.database import get_db
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_token(data:dict):
    token=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token



def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,SECRET_KEY,algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
         raise HTTPException(
              status_code=401,
              detail="Invalid or expired token"
         )



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    
        payload=verify_token(token)
        user_id=payload.get("sub")


        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        current_user = db.execute(
    select(users).where(users.id == int(user_id))
                ).scalar_one_or_none()
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return current_user
        
 