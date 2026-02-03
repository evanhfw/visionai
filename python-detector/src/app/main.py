import cv2
from app.adapters.video.rtsp_stream import RTSPStream
from app.adapters.vision.yolo_detector import YOLODetector
from app.usecases.detect_objects import DetectObjects

def main():
    stream = RTSPStream("rtsp://localhost:8554/cam1")
    detector = YOLODetector()
    usecase = DetectObjects(detector)

    while True:
        ret, frame = stream.read()
        if not ret:
            continue

        detections = usecase.execute(frame)

        for d in detections:
            x1, y1, x2, y2 = d.bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{d.label} {d.confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
