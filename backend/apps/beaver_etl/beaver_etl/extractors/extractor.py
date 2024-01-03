from abc import ABC, abstractmethod
from pathlib import Path

from beaver_etl.extractors.schema import ExtractorCodeSchema


class IExtractor(ABC):
    @abstractmethod
    def extract(self, dataset: Path) -> list[ExtractorCodeSchema]:
        ...


class PythonPoetryExtractor(IExtractor):
    def extract(self, dataset: Path) -> list[ExtractorCodeSchema]:
        raise NotImplementedError
