from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import Project
from app.schemas.project import ProjectCreate


class ProjectRepository:
    @staticmethod
    def create_project(db: Session, project: ProjectCreate, owner_id: int):
        try:
            db_project = Project(
                owner_id=owner_id,
                name=project.name,
                url=project.url,
                language_id=project.language_id
            )
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return db_project
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error occurred while creating project: {str(e)}")

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 10):
        try:
            return db.query(Project).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Error occurred while fetching projects: {str(e)}")

    @staticmethod
    def get_project_by_id(db: Session, project_id: int):
        try:
            return db.query(Project).filter(Project.id == project_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Error occurred while fetching project by ID: {str(e)}")

    @staticmethod
    def delete_project(db: Session, project_id: int):
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.deleted_at = datetime.utcnow()
                db.commit()
                return project
            else:
                raise Exception("Project not found.")
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error occurred while deleting project: {str(e)}")
