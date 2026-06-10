from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.court import Court
from app.models.booking import Booking
from app.routers.auth import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
async def read_root():
    return {"Hello": "World"}