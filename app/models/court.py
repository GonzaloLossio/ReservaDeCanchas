from sqlmodel import SQLModel, Field

class Court(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    sport: str
    price_per_hour: float 
    is_active: bool = True
    location: str