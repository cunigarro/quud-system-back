from typing import List
import os

from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule
from app.db.enums import LanguageEnum
from app.schemas.inspections import Comment
from app.components.drivers.implementation_all_classes import (
    PythonDriver,
    JavaDriver,
    JavaScriptDriver
)


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
                f"Driver required_classes not implemented for: {language}"
            )

    def execute(self, context):
        print("[required_classes] Verificando clases requeridas...")

        language: LanguageEnum = context["language"]
        code_path: str = context['data']['fetch_code']['repository_path']
        files: List[str] = context['data']['fetch_code']['files']

        driver = self.get_driver(language)

        total_defined_classes = 0
        comments: List[Comment] = []

        for file_path in files:
            full_path = os.path.join(code_path, file_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(
                    f"[ERROR] can not read: {file_path}, error: {str(e)}"
                )
                continue

            defined = driver.get_defined_classes(content)
            total_defined_classes += len(defined)

        if total_defined_classes == 0:
            calification = 1
            description = """
                No classes were found defined in the project.
                You must create at least one class.
            """
            comments.append(
                Comment(
                    description=description,
                    path_file=None
                )
            )
        else:
            calification = 100

        self.save_quality_result(
            context=context,
            calification=calification,
            message=f"{total_defined_classes} classes were found defined.",
            details={"defined_classes": total_defined_classes},
            comments=comments
        )

        context["required_classes_found"] = total_defined_classes > 0
        return context
