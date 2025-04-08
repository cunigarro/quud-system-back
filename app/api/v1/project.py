from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.project import ProjectCreate
from app.services.project_service import ProjectService
from app.core.security import get_current_user
from app.schemas.response import StandardResponse
from app.db.models import User

router = APIRouter()


@router.post("/", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project_data = ProjectService.create_project(
        db=db,
        project=project,
        owner_id=current_user.id
    )
    return StandardResponse(message="Project created successfully", data=project_data)


@router.get("/", response_model=StandardResponse)
def get_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = ProjectService.get_projects(current_user, db=db, skip=skip, limit=limit)
    return StandardResponse(
        message="Projects fetched successfully",
        data=projects
    )


@router.get("/{project_id}", response_model=StandardResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = ProjectService.get_project_by_id(db=db, project_id=project_id)
    return StandardResponse(
        message="Project fetched successfully",
        data=project
    )


@router.delete("/{project_id}", response_model=StandardResponse, status_code=status.HTTP_200_OK)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ProjectService.delete_project(db=db, project_id=project_id)
    return StandardResponse(message="Project deleted successfully")
