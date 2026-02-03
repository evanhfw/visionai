import subprocess
from typing import Optional

from app.domain.frame import Frame


class RTSPWriter:
    """RTSP stream writer using ffmpeg with GPU encoding (NVENC)."""

    def __init__(
        self,
        url: str,
        width: int,
        height: int,
        fps: int = 30,
        bitrate: str = "4M",
    ):
        self.url = url
        self.width = width
        self.height = height
        self.fps = fps
        self.bitrate = bitrate
        self._process: Optional[subprocess.Popen] = None
        self._start_ffmpeg()

    def _start_ffmpeg(self) -> None:
        """Start ffmpeg subprocess with NVENC GPU encoder."""
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),
            "-i", "pipe:0",
            # GPU encoding with NVENC
            "-c:v", "h264_nvenc",
            "-preset", "p4",  # balanced preset for low latency
            "-tune", "ll",  # low latency tuning
            "-b:v", self.bitrate,
            "-maxrate", self.bitrate,
            "-bufsize", self.bitrate,
            "-g", str(self.fps * 2),  # keyframe interval
            # RTSP output
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            self.url,
        ]

        self._process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def write(self, frame: Frame) -> bool:
        """Write a frame to the RTSP stream.

        Args:
            frame: Frame object containing the image to write.

        Returns:
            True if write succeeded, False otherwise.
        """
        if self._process is None or self._process.stdin is None:
            return False

        try:
            self._process.stdin.write(frame.image.tobytes())
            return True
        except BrokenPipeError:
            return False

    def release(self) -> None:
        """Release ffmpeg subprocess resources."""
        if self._process is not None:
            if self._process.stdin:
                self._process.stdin.close()
            self._process.wait()
            self._process = None
