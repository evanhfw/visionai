from pydantic import BaseModel

class BBox(BaseModel):
    x_min: int
    y_min: int
    x_max: int
    y_max: int