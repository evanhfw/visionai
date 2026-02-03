from pydantic import BaseModel


class BBox(BaseModel):
    """Bounding box with x_min, y_min, x_max, y_max coordinates."""

    x_min: int
    y_min: int
    x_max: int
    y_max: int

    @property
    def width(self) -> int:
        return self.x_max - self.x_min

    @property
    def height(self) -> int:
        return self.y_max - self.y_min

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def center(self) -> tuple[int, int]:
        return (self.x_min + self.x_max) // 2, (self.y_min + self.y_max) // 2

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Return as (x_min, y_min, x_max, y_max) tuple."""
        return self.x_min, self.y_min, self.x_max, self.y_max
