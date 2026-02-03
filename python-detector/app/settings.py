from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    STREAM_RELAY_RTSP_URL: str
    VEHICLE_DETECTOR_MODEL_PATH: str

load_dotenv()
settings = Settings()