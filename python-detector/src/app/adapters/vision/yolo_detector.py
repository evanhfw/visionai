from ultralytics import YOLO
from app.domain.detection import Detection
from app.usecases.ports import ObjectDetectorPort

class YOLODetector(ObjectDetectorPort):
    def __init__(self, model_path="yolo26m.pt", conf=0.4):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        results = self.model(frame, conf=self.conf, verbose=False)
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
                        bbox=(x1, y1, x2, y2),
                    )
                )

        return detections
