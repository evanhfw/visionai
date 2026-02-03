from abc import ABC, abstractmethod
from typing import List
from app.domain.detection import Detection

class ObjectDetectorPort(ABC):
    @abstractmethod
    def detect(self, frame) -> List[Detection]:
        pass
