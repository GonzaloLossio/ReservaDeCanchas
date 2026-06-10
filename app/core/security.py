import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise ValueError("Invalid token")
    
async def get_current_user(token : str = Depends(oauth2_scheme), db : AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if not username:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=401, detail="Token Invalido")  

    result = await db.execute(select(User).where(User.username == username)) 
    valid_user = result.scalars().first()
    if not valid_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return valid_user