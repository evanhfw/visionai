from typing import List
from app.domain.detection import Detection
from app.usecases.ports import ObjectDetectorPort

class DetectObjects:
    def __init__(self, detector: ObjectDetectorPort):
        self.detector = detector

    def execute(self, frame) -> List[Detection]:
        return self.detector.detect(frame)
