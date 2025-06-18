from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import Depends,HTTPException, status, FastAPI
from passlib.context import CryptContext
from sqlalchemy.orm import Session, Mapped
from jose import JWTError, jwt
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Annotated
from models import User
from PYD.users import UserReturn
from database import get_db
  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 200

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

#
#   HASH LOGIC
#


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

#
#   USER LOGIC
#


def get_user(username: str, db:Session):
    return db.query(User).filter(User.username==username).first()

def authenticate_user(username: str, password: str, db:Session=Depends(get_db)):
    user = get_user(username,db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db))->UserReturn:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    except Exception as e:
        credentials_exception.detail='Signature has expired. Please reauthorize'
        raise credentials_exception
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#
#   TOKEN LOGIC
#

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get("sub")
        if username is None:
            raise HTTPException(403, "Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(403, "Token is invalid or expired")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#
#   ROLE LOGIc
#

class RoleChecker:  
  def __init__(self, allowed_roles):  
    self.allowed_roles = allowed_roles  
  
  def __call__(self, user: Annotated[UserReturn, Depends(get_current_user)]):  
    if user.role in self.allowed_roles:  
      return user 
    raise HTTPException(401, detail="You don't have enough permissions")
  
def is_admin(role):
    if role=='admin':
        return True
    else:
        return False