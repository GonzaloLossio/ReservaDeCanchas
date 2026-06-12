from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from sqlmodel import select
from app.core.security import get_current_user
from app.models import Booking, Court
from app.schemas.booking import BookingCreate, BookingResponse
from datetime import datetime
from app.services.booking_services import calculate_price

router = APIRouter()

@router.post('/bookings', response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Court).where(Court.id == booking.court_id, Court.is_active == True))
    court = result.scalars().first()
    if not court:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    
    await db.execute(text("SELECT pg_advisory_xact_lock(:court_id)"), {"court_id": booking.court_id})
    
    overlap = await db.execute(
        select(Booking).where(
            Booking.court_id == booking.court_id,
            Booking.date == booking.date,
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time,
            Booking.status == "confirmed"
        )
    )
    existing_booking = overlap.scalars().first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="La cancha ya está reservada para ese horario")
    

    total_price = calculate_price(court.price_per_hour, booking.start_time, booking.end_time, booking.date)

    new_booking = Booking(
        user_id = current_user.id,
        court_id = booking.court_id,
        start_time = booking.start_time,
        end_time = booking.end_time,
        total_price = total_price,
        date = booking.date
    )

    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return new_booking


@router.get('/bookings',response_model = list[BookingResponse])
async def get_bookings(db : AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    result = await db.execute(select(Booking).where(Booking.user_id == current_user.id))
    all_bookings = result.scalars().all()
    return all_bookings

@router.delete('/bookings/{booking_id}',response_model = BookingResponse)
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id))
    booking_to_delete = result.scalars().first()
    if not booking_to_delete:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    booking_date_time = datetime.combine(booking_to_delete.date, booking_to_delete.start_time)
    if (booking_date_time - datetime.utcnow()).total_seconds() < 7200:
        raise HTTPException(status_code=400, detail="No se pueden cancelar reservas con menos de 2 horas de anticipación")
    
    booking_to_delete.status = "cancelled"
    await db.commit()
    await db.refresh(booking_to_delete)

    return booking_to_delete