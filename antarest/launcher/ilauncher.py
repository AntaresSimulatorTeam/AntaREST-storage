from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID

from antarest.common.config import Config
from antarest.launcher.model import ExecutionResult


class ILauncher(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def run_study(self, study_path: Path, version: str) -> UUID:
        pass

    @abstractmethod
    def get_result(self, uuid: UUID) -> ExecutionResult:
        pass
