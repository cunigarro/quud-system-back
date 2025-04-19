import os

from app.components.base_rule import BaseRule
from app.db.enums import LanguageEnum, ResultStatusEnum


class CodeLanguageValidator:
    def __init__(self, code_path: str):
        self.code_path = code_path

        if not os.path.isdir(self.code_path):
            raise FileNotFoundError(
                f"Path not found: {self.code_path}"
            )

    def has_valid_code(self, language: LanguageEnum) -> bool:
        if language == LanguageEnum.java:
            return self._contains_files_with_extension(".java")
        elif language == LanguageEnum.python:
            return self._contains_files_with_extension(".py")
        else:
            raise ValueError(f"Unsupported language: {language}")

    def _contains_files_with_extension(self, extension: str) -> bool:
        for root, _, files in os.walk(self.code_path):
            for file in files:
                if file.endswith(extension):
                    return True
        return False


class RuleHandler(BaseRule):
    def execute(self, context):
        language: LanguageEnum = context["language"]
        code_path: str = context['data']['fetch_code']['repository_path']

        if not code_path:
            print("No code to evaluate")
            return context

        validator = CodeLanguageValidator(code_path)
        check_language = validator.has_valid_code(language)

        if not check_language:
            self.save_result({
                'inspection_status': ResultStatusEnum.VALIDATION_ERROR,
                'validations': 'Code no detected in the repository and branch'
            })
            raise ValueError(f"Language is not detected: {language}")

        context["validations_passed"] = check_language

        return context
