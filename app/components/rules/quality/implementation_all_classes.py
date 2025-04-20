import os
from typing import List, Optional
import re

from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule
from app.schemas.inspections import Comment
from app.db.enums import LanguageEnum
from app.components.drivers.implementation_all_classes import (
    PythonDriver,
    JavaDriver,
    JavaScriptDriver
)

rule_name = 'implementation_all_classes'


class RuleHandler(BaseRule, BaseQualityRule):
    def get_driver(self, language: LanguageEnum):
        if language == LanguageEnum.python:
            return PythonDriver()
        elif language == LanguageEnum.java:
            return JavaDriver()
        elif language == LanguageEnum.javascript:
            return JavaScriptDriver()
        else:
            raise ValueError(
                f"Driver {rule_name} not implemented for: {language}"
            )

    def execute(self, context):
        print(f"[{rule_name}] Verificando clases implementadas...")

        language: LanguageEnum = context["language"]
        code_path: str = context['data']['fetch_code']['repository_path']
        files: List[str] = context['data']['fetch_code']['files']

        driver = self.get_driver(language)

        total_classes = 0
        implemented_classes = 0
        comments: List[Comment] = []

        for file_path in files:
            result = self._process_file(code_path, file_path, driver)
            if not result:
                continue

            defined, implemented, file_comments = result
            total_classes += len(defined)
            implemented_classes += len(implemented)
            comments.extend(file_comments)

        calification = (
            implemented_classes / total_classes
        ) * 100 if total_classes else 1

        message = f"""{implemented_classes} of {total_classes}
            classes were implemented.
        """
        self.save_quality_result(
            context=context,
            calification=calification,
            message=message,
            details={
                "implemented": implemented_classes,
                "total": total_classes
            },
            comments=comments
        )

        context["implementation_all_classes"] = True
        return context

    def find_class_line(self, content: str, class_name: str) -> int:
        pattern = rf"\bclass\s+{re.escape(class_name)}\b"
        for i, line in enumerate(content.splitlines(), start=1):
            if re.search(pattern, line):
                return i
        return -1

    def _process_file(
        self,
        code_path: str,
        file_path: str,
        driver
    ) -> Optional[tuple]:
        full_path = os.path.join(code_path, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] can not open: {file_path}, error: {str(e)}")
            return None

        defined = driver.get_defined_classes(content)
        implemented = driver.get_implemented_classes(content)

        comments = [
            Comment(
                line_start=str(line_num) if line_num else None,
                line_end=str(line_num) if line_num else None,
                path_file=file_path,
                description=f"""
                    The class '{class_name}' is defined but not
                    implemented correctly.
                """
            )
            for class_name in defined
            if class_name not in implemented
            for line_num in [self.find_class_line(content, class_name)]
        ]

        return defined, implemented, comments
