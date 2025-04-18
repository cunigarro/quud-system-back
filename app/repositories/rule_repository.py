from sqlalchemy.orm import Session, joinedload

from app.db.models import Rule, RuleGroup, RuleGroupRule


class RuleRepository:
    @staticmethod
    def get_all_rules(db: Session):
        return db.query(Rule).filter(Rule.deleted_at.is_(None)).all()

    @staticmethod
    def create_group(db: Session, name: str, description: str, owner_id: int, rule_ids: list, flow_config=dict):
        group = RuleGroup(
            name=name,
            description=description,
            owner_id=owner_id,
            flow_config=flow_config
        )
        db.add(group)
        db.commit()
        db.refresh(group)

        for rule_id in rule_ids:
            link = RuleGroupRule(rule_id=rule_id, group_id=group.id)
            db.add(link)

        db.commit()
        return group

    @staticmethod
    def get_groups_by_user(db: Session, user_id: int):
        return (
            db.query(RuleGroup)
            .options(joinedload(RuleGroup.group_rules).joinedload(RuleGroupRule.rule))
            .filter(RuleGroup.owner_id == user_id, RuleGroup.deleted_at.is_(None))
            .all()
        )
