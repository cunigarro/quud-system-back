from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.project import ProjectCreate, ProjectResponse
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    @staticmethod
    def create_project(db: Session, project: ProjectCreate, owner_id: int) -> ProjectResponse:
        try:
            db_project = ProjectRepository.create_project(
                db,
                project,
                owner_id
            )
            return ProjectResponse.from_orm(db_project)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Project creation failed: {str(e)}"
            )

    @staticmethod
    def get_projects(owner_id: int, db: Session, skip: int = 0, limit: int = 10) -> list[ProjectResponse]:
        try:
            projects = ProjectRepository.get_projects(owner_id, db, skip, limit)
            return [ProjectResponse.from_orm(project) for project in projects]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch projects: {str(e)}"
            )

    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> ProjectResponse:
        try:
            db_project = ProjectRepository.get_project_by_id(db, project_id)
            if db_project is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )
            return ProjectResponse.from_orm(db_project)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch project: {str(e)}"
            )

    @staticmethod
    def delete_project(db: Session, project_id: int):
        try:
            deleted_project = ProjectRepository.delete_project(db, project_id)
            if deleted_project:
                return {"message": "Project soft-deleted successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete project: {str(e)}"
            )
