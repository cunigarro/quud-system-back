import importlib
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.db.models import Inspection, Rule, RuleGroupRule
from .base_rule import BaseRule


class Orchestrator:
    def __init__(self, db: Session, inspection: Inspection):
        self.db = db
        self.inspection = inspection
        self.execution_result = {
            "steps": [],
            "success": True,
        }
        self.context = {
            "inspection": inspection,
            "data": {},
            "db": self.db
        }

    def _load_rule_handler(self, rule_name: str, scope: str):
        try:
            module_path = f"app.components.rules.{scope}.{rule_name}"
            print(module_path)
            module = importlib.import_module(module_path)
            return getattr(module, "RuleHandler")()
        except ModuleNotFoundError:
            raise ImportError(
                f"Rule component '{rule_name}' not found in components.rules."
            )
        except AttributeError:
            raise ImportError(
                f"'RuleHandler' class not found in {rule_name}.py"
            )

    def _get_rules_by_group(self) -> List[Rule]:
        return (
            self.db.query(Rule)
            .join(RuleGroupRule, Rule.id == RuleGroupRule.rule_id)
            .filter(RuleGroupRule.group_id == self.inspection.rule_group.id)
            .all()
        )

    def run_flow(
        self,
        flow: List[Dict[str, Any]],
        flow_scope: str = "general"
    ) -> bool:
        for step in flow:
            rule_name = step["name"]
            settings = step.get("settings", {})

            if not rule_name:
                self.execution_result["steps"].append({
                    "rule": rule_name,
                    "scope": flow_scope,
                    "status": "skipped",
                    "error": "Missing rule name"
                })
                continue

            try:
                handler: BaseRule = self._load_rule_handler(
                    rule_name, flow_scope
                )
                handler.configure(settings)
                handler.execute(self.context)

                self.execution_result["steps"].append({
                    "rule": rule_name,
                    "scope": flow_scope,
                    "status": "success"
                })

            except Exception as e:
                self.execution_result["steps"].append({
                    "rule": rule_name,
                    "scope": flow_scope,
                    "status": "error",
                    "error": str(e)
                })
                return False

        return True

    def execute_inspection(self):
        if not self.inspection.rule_group:
            raise ValueError("Inspection has no rule group assigned.")

        flow_config = self.inspection.rule_group.flow_config or {}
        rules = self._get_rules_by_group()

        # Run init_flow (general)
        success = self.run_flow(
            flow_config.get("init_flow", []), flow_scope="general"
        )
        if not success:
            self.run_flow(
                flow_config.get("on_error", []), flow_scope="general"
            )
            self.execution_result["success"] = False
            return self.execution_result

        # Run init_flow for each rule
        for rule in rules:
            rule_flow = rule.flow_config or {}
            rule_success = self.run_flow(
                rule_flow.get("init_flow", []), flow_scope="quality"
            )
            if not rule_success:
                success = False

        # Run finish_flow if everything ok
        if success:
            finish_success = self.run_flow(
                flow_config.get("finish_flow", []), flow_scope="general"
            )
            success = success and finish_success

        # If something failed, run on_error
        if not success:
            self.run_flow(
                flow_config.get("on_error", []), flow_scope="general"
            )
            self.execution_result["success"] = False

        return self.execution_result
