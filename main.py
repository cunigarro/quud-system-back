from fastapi import FastAPI

from app.api import auth
from app.api import language
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(language.router, prefix="/api")
