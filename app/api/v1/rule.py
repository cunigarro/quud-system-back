from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.rule_service import RuleService
from app.schemas.rule import RuleGroupCreate
from app.schemas.response import StandardResponse
from app.db.database import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.get("/rules", response_model=StandardResponse)
def list_rules(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    rules = RuleService(db).get_all_rules()
    return StandardResponse(message="Rules fetched", data={"rules": rules})


@router.post("/rules/groups", response_model=StandardResponse)
def create_group(payload: RuleGroupCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = RuleService(db).create_group(current_user.id, payload)
    return StandardResponse(message="Group created", data={"group": group})


@router.get("/rules/groups", response_model=StandardResponse)
def get_user_groups(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    groups = RuleService(db).get_user_groups(current_user.id)
    return StandardResponse(message="Groups fetched", data={"groups": groups})
