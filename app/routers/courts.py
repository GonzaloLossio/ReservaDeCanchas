from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlmodel import select
from app.core.security import get_admin_user
from app.models import Court
from app.schemas.court import CourtCreate, CourtResponse

router = APIRouter()

@router.post('/courts', response_model=CourtResponse)
async def create_court(court: CourtCreate, db: AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    new_court = Court(
        name = court.name,
        location = court.location,
        price_per_hour = court.price_per_hour,
        sport = court.sport
    )

    db.add(new_court)
    await db.commit()
    await db.refresh(new_court)

    return new_court

@router.get('/courts', response_model=list[CourtResponse])
async def get_courts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Court).where(Court.is_active == True))
    courts = result.scalars().all()
    return courts


@router.get('/courts/{court_id}', response_model=CourtResponse)
async def get_court(court_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Court).where(Court.id == court_id))
    court = result.scalars().first()
    if not court:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    return court

@router.put('/courts/{court_id}', response_model=CourtResponse)
async def update_court(court_id: int, court_update: CourtCreate, db: AsyncSession = Depends(get_db), admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Court).where(Court.id == court_id))
    court = result.scalars().first()
    if not court:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")

    for key, value in court_update.dict().items():
        setattr(court, key, value)

    await db.commit()
    await db.refresh(court)

    return court

@router.delete('/courts/{court_id}')
async def delete_court(court_id : int, db:AsyncSession = Depends(get_db),admin_user = Depends(get_admin_user)):
    result = await db.execute(select(Court).where(Court.id == court_id))
    court = result.scalars().first()
    if not court:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")

    court.is_active = False
    await db.commit()
    await db.refresh(court)

    return {"detail": "Cancha desactivada exitosamente"}