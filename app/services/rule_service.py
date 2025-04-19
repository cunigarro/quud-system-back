import json
import os

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.rule_repository import RuleRepository
from app.schemas.rule import RuleGroupCreate, RuleResponse
from app.schemas.rule_group import RuleGroupResponse


class RuleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_rules(self):
        try:
            rules = RuleRepository.get_all_rules(self.db)
            return [RuleResponse.from_orm(rule) for rule in rules]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch rules: {str(e)}"
            )

    def load_flow_config_from_file(self, filename: str) -> dict:
        base_path = os.path.join("app", "db", "defaults")
        file_path = os.path.join(base_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_group(self, user_id: int, data: RuleGroupCreate):
        try:
            flow_config = self.load_flow_config_from_file(
                "default_flow_config.json"
            )

            db_group = RuleRepository.create_group(
                db=self.db,
                name=data.name,
                description=data.description,
                owner_id=user_id,
                rule_ids=data.rule_ids,
                flow_config=flow_config
            )
            return RuleGroupResponse.from_orm(db_group)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Project creation failed: {str(e)}"
            )

    def get_user_groups(self, user_id: int):
        groups = RuleRepository.get_groups_by_user(self.db, user_id)
        return [
            RuleGroupResponse.from_orm(group) for group in groups
        ]
