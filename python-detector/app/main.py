import cv2

from app.adapters.video.rtsp_stream import RTSPStream
from app.adapters.vision.yolo_detector import YOLODetector
from app.settings import settings
from app.usecases.detect_objects import DetectObjects

# Drawing constants
BBOX_COLOR = (0, 255, 0)
FONT_SCALE = 0.6
THICKNESS = 2


def main() -> None:
    """Entry point for object detection pipeline."""
    stream = RTSPStream(settings.STREAM_RELAY_RTSP_URL)
    detector = YOLODetector(settings.VEHICLE_DETECTOR_MODEL_PATH)
    usecase = DetectObjects(detector)

    try:
        while True:
            frame = stream.read()
            if frame is None:
                continue

            detections = usecase.execute(frame)

            for d in detections:
                x1, y1, x2, y2 = d.bbox.as_tuple()
                cv2.rectangle(frame.image, (x1, y1), (x2, y2), BBOX_COLOR, THICKNESS)
                cv2.putText(
                    frame.image,
                    f"{d.label} {d.confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SCALE,
                    BBOX_COLOR,
                    THICKNESS,
                )

            cv2.imshow("Detector", frame.image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stream.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
