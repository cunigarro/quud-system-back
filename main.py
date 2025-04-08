from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    auth,
    language,
    project,
    rule,
    inspection
)
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quud",
    description="API for managing the quality Code",
    version="1.0.0"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Quud",
        version="1.0.0",
        description="API for managing the quality Code",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(language.router, prefix="/api/v1/languages", tags=["languages"])
app.include_router(project.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(rule.router, prefix="/api/v1/rules", tags=["rules"])
app.include_router(inspection.router, prefix="/api/v1/inspections", tags=["inspections"])
