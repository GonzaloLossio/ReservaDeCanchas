from sqlmodel import SQLModel
from datetime import date,time,datetime

class BookingCreate(SQLModel):
    start_time: time
    end_time: time
    date: date
    court_id: int

class BookingResponse(SQLModel):
    id: int
    user_id: int 
    court_id: int 
    start_time: time
    end_time: time
    total_price: float
    date: date
    created_at: datetime 
    status: str   