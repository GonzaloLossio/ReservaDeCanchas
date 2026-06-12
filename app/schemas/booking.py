from sqlmodel import SQLModel
from datetime import date,time,datetime
from pydantic import model_validator

class BookingCreate(SQLModel):
    start_time: time
    end_time: time
    date: date
    court_id: int

    @model_validator(mode='after')
    def check_times(self):
        if self.start_time >= self.end_time:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin")
        return self

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