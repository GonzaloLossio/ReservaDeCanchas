from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.court import Court
from app.models.booking import Booking
from app.routers.auth import router as auth_router
from app.routers.courts import router as courts_router
from app.routers.booking import router as booking_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(courts_router)
app.include_router(booking_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def read_root():
    return {"Hello": "World"}