from fastapi import FastAPI

from app.api.v1 import (
    auth,
    language,
    project
)
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quud",
    description="API for managing the quality Code",
    version="1.0.0"
)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(language.router, prefix="/api/v1", tags=["languages"])
app.include_router(project.router, prefix="/api/v1", tags=["projects"])
