from sqlmodel import SQLModel

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserLogin(SQLModel):
    username: str
    password: str    

class UserResponse(SQLModel):
    id: int 
    username: str
    email: str
    role: str
    is_active : bool = True