from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate,UserLogin,UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlmodel import select
from app.models.user import User
from app.core.security import hash_password,verify_password,create_access_token,get_current_user

router = APIRouter()

@router.post('/register',response_model=UserResponse)
async def register(user: UserCreate, db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user: 
        raise HTTPException(status_code = 400, detail="El usuario ya existe")
    
    result = await db.execute(select(User).where(User.email == user.email))
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(status_code=400, detail="El Email ya ha sido registrado")
    hashed_password = hash_password(user.password)
    
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post('/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    correct_username = result.scalars().first()
    if not correct_username:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    correct_password = verify_password(form_data.password,correct_username.hashed_password)
    if not correct_password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas") 
    
    access_token = create_access_token(data = {"sub": correct_username.username})

    return {"access_token" : access_token, "token_type": "bearer"}


@router.get('/me', response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user