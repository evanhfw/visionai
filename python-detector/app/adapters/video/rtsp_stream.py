from datetime import datetime

import cv2

from app.domain.frame import Frame


class RTSPStream:
    """RTSP video stream adapter that produces Frame objects."""

    def __init__(self, url: str, source_id: str | None = None):
        self.url = url
        self.source_id = source_id or self._extract_source_id(url)
        self.cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        self._frame_counter = 0

    @staticmethod
    def _extract_source_id(url: str) -> str:
        """Extract a safe identifier from URL (without credentials)."""
        # Remove protocol
        if "://" in url:
            url = url.split("://", 1)[1]
        # Remove credentials if present
        if "@" in url:
            url = url.split("@", 1)[1]
        # Take first part (host:port/path)
        return url.split("/")[0] if "/" in url else url

    def read(self) -> Frame | None:
        """Read a frame from the stream. Returns None if read fails."""
        ret, image = self.cap.read()
        if not ret:
            return None

        self._frame_counter += 1
        height, width = image.shape[:2]

        return Frame(
            frame_id=self._frame_counter,
            timestamp=datetime.now(),
            source=self.source_id,
            resolution=(width, height),
            image=image,
        )

    def release(self) -> None:
        """Release the video capture resource."""
        self.cap.release()
