from datetime import datetime

import numpy as np
from pydantic import BaseModel, ConfigDict


class Frame(BaseModel):
    """Represents a video frame with metadata."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    frame_id: int
    timestamp: datetime
    source: str
    resolution: tuple[int, int]
    image: np.ndarray
