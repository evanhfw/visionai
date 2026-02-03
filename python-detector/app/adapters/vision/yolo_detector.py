import numpy as np
from ultralytics import YOLO

from app.domain.bbox import BBox
from app.domain.detection import Detection
from app.usecases.ports import ObjectDetectorPort


class YOLODetector(ObjectDetectorPort):
    """YOLO-based object detector adapter."""

    def __init__(self, model_path: str = "yolo26m.pt", conf: float = 0.4):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, image: np.ndarray) -> list[Detection]:
        """Detect objects in an image using YOLO.

        Args:
            image: numpy array representing the image (BGR format)

        Returns:
            List of Detection objects found in the image
        """
        results = self.model(image, conf=self.conf, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append(
                    Detection(
                        label=label,
                        confidence=confidence,
                        bbox=BBox(x_min=x1, y_min=y1, x_max=x2, y_max=y2),
                    )
                )

        return detections
