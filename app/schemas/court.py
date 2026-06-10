from sqlmodel import SQLModel

class CourtCreate(SQLModel):
    name : str
    sport: str
    price_per_hour: float 
    location: str

class CourtResponse(SQLModel):
    id: int 
    name: str 
    sport: str
    price_per_hour: float 
    is_active: bool = True
    location: str