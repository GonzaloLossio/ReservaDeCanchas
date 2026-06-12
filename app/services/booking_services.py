from datetime import datetime,time
from app.models.booking import Booking
from app.models.court import Court


def calculate_price(price_per_hour: float, start_time: time, end_time: time,date) -> float:
    hours = (datetime.combine(date, end_time) - datetime.combine(date, start_time)).seconds / 3600

    if date.weekday() >= 5:
        price_per_hour *= 1.2

    if time(18,0) <= start_time:
        price_per_hour *= 1.5

    return hours * price_per_hour    
    
    

    
    