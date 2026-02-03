import datetime
from typing import Any

from pydantic import BaseModel

class Frame(BaseModel):
    timestamp: datetime
    image: Any
