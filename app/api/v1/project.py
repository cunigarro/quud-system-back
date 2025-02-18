from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService
from app.core.security import get_current_user

router = APIRouter()


@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return ProjectService.create_project(db=db, project=project, owner_id=current_user.id)

@router.get("/projects/", response_model=list[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return ProjectService.get_projects(db=db, skip=skip, limit=limit)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService.get_project_by_id(db=db, project_id=project_id)

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService.delete_project(db=db, project_id=project_id)