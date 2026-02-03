from pydantic import BaseModel

from app.domain.bbox import BBox


class Detection(BaseModel):
    """Represents a detected object with label, confidence, and bounding box."""

    label: str
    confidence: float
    bbox: BBox
