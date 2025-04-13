from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseDriver(ABC):
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings

    @abstractmethod
    def execute(self, context: Dict[str, Any]):
        pass
