from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    STREAM_RELAY_RTSP_URL: str
    VEHICLE_DETECTOR_MODEL_PATH: str
    STREAM_RTSP_OUT_URL: str

    # Drawing constants
    BBOX_COLOR: str = "0,255,0"
    FONT_SCALE: float = 0.6
    THICKNESS: int = 2

    def get_bbox_color_tuple(self) -> tuple[int, int, int]:
        """Parse BBOX_COLOR string to BGR tuple."""
        r, g, b = map(int, self.BBOX_COLOR.split(","))
        return (b, g, r)  # OpenCV uses BGR


settings = Settings()