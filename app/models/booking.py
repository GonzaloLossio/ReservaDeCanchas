from sqlmodel import SQLModel, Field
from datetime import date,time,datetime

class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    court_id: int = Field(foreign_key="court.id")
    start_time: time
    end_time: time
    total_price: float
    date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="confirmed")