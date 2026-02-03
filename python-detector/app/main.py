import cv2

from app.adapters.video.rtsp_stream import RTSPStream
from app.adapters.video.rtsp_writer import RTSPWriter
from app.adapters.vision.yolo_detector import YOLODetector
from app.settings import settings
from app.usecases.detect_objects import DetectObjects
from app.utils.fps_counter import FPSCounter


def main() -> None:
    """Entry point for object detection pipeline."""
    stream = RTSPStream(settings.STREAM_RELAY_RTSP_URL)
    detector = YOLODetector(settings.VEHICLE_DETECTOR_MODEL_PATH)
    usecase = DetectObjects(detector)

    # Get drawing constants from settings
    bbox_color = settings.get_bbox_color_tuple()
    font_scale = settings.FONT_SCALE
    thickness = settings.THICKNESS

    # Initialize writer after first frame to get resolution
    writer: RTSPWriter | None = None
    fps_counter = FPSCounter()

    try:
        while True:
            frame = stream.read()
            if frame is None:
                continue

            # Initialize writer on first frame
            if writer is None:
                width, height = frame.resolution
                writer = RTSPWriter(
                    url=settings.STREAM_RTSP_OUT_URL,
                    width=width,
                    height=height,
                )

            detections = usecase.execute(frame)

            for d in detections:
                x1, y1, x2, y2 = d.bbox.as_tuple()
                cv2.rectangle(frame.image, (x1, y1), (x2, y2), bbox_color, thickness)
                cv2.putText(
                    frame.image,
                    f"{d.label} {d.confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    bbox_color,
                    thickness,
                )

            # Draw FPS counter (top-left corner)
            fps = fps_counter.tick()
            cv2.putText(
                frame.image,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                bbox_color,
                thickness,
            )

            # Push frame to RTSP output
            writer.write(frame)

            cv2.imshow("Detector", frame.image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stream.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
