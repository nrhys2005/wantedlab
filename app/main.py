from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import db
from app.api.routers import register_routers
from app.db import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=db.engine)
    yield

app = FastAPI(lifespan=lifespan)
register_routers(app)

