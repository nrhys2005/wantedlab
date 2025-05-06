from fastapi import FastAPI

from app import db
from app.api.routes import companies, tags
from app.db import Base

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=db.engine)

app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(tags.router, prefix="/companies", tags=["tags"])
