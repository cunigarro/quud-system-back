import re
from abc import ABC, abstractmethod
from typing import List
import ast


class BaseLanguageDriver(ABC):

    @abstractmethod
    def get_defined_classes(self, file_content: str) -> List[str]:
        pass

    @abstractmethod
    def get_implemented_classes(self, file_content: str) -> List[str]:
        pass


class PythonDriver(BaseLanguageDriver):
    def get_defined_classes(self, file_content: str):
        return [node.name for node in ast.walk(ast.parse(file_content)) if isinstance(node, ast.ClassDef)]

    def get_implemented_classes(self, file_content: str):
        implemented = []
        for node in ast.walk(ast.parse(file_content)):
            if isinstance(node, ast.ClassDef) and any(isinstance(n, ast.FunctionDef) for n in node.body):
                implemented.append(node.name)
        return implemented


class JavaDriver(BaseLanguageDriver):
    def get_defined_classes(self, file_content: str):
        return re.findall(r'\b(?:public\s+|abstract\s+)?class\s+(\w+)', file_content)

    def get_implemented_classes(self, file_content: str):
        implemented = []
        class_defs = re.finditer(r'\b(?:public\s+|abstract\s+)?class\s+(\w+)\s*{', file_content)

        for match in class_defs:
            class_body_start = match.end()
            class_body = file_content[class_body_start:]

            limited_body = class_body[:1000]
            if re.search(r'\b(public|private|protected)\s+[\w<>]+\s+\w+\s*\([^)]*\)\s*{', limited_body):
                implemented.append(match.group(1))

        return implemented


class JavaScriptDriver(BaseLanguageDriver):
    def get_defined_classes(self, file_content: str):
        return re.findall(r'\bclass\s+(\w+)', file_content)

    def get_implemented_classes(self, file_content: str):
        implemented = []
        class_defs = re.finditer(r'class\s+(\w+)\s*{', file_content)

        for match in class_defs:
            class_body_start = match.end()
            class_body = file_content[class_body_start:]

            limited_body = class_body[:1000]
            if re.search(r'\b\w+\s*\([^)]*\)\s*{', limited_body):
                implemented.append(match.group(1))

        return implemented
