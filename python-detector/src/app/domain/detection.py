from pydantic import BaseModel, Field

from app.domain.bbox import BBox

class Detection(BaseModel):
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
