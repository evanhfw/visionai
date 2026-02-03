from app.domain.detection import Detection
from app.domain.frame import Frame
from app.usecases.ports import ObjectDetectorPort


class DetectObjects:
    """Use case for detecting objects in a frame."""

    def __init__(self, detector: ObjectDetectorPort):
        self.detector = detector

    def execute(self, frame: Frame) -> list[Detection]:
        """Execute object detection on the given frame.

        Args:
            frame: Frame object containing image and metadata

        Returns:
            List of Detection objects found in the frame
        """
        return self.detector.detect(frame.image)
