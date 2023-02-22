from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
# from .config import settings
from dotenv import load_dotenv
import os

load_dotenv()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = os.getenv('OAUTH_SECRET')
ALGORITHM = os.getenv('OAUTH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_TIME = os.getenv('ACCESS_TOKEN_EXPIRE_TIME')


def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_TIME))
    to_encode.update({"exp" : expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:  
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.email == token.email).first()

    return user
