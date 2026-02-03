import time
from collections import deque


class FPSCounter:
    """Smoothed FPS counter using rolling average."""

    def __init__(self, window_size: int = 30):
        """Initialize FPS counter.

        Args:
            window_size: Number of samples for rolling average.
                         Default 30 = ~1 second window at 30fps.
        """
        self._history: deque[float] = deque(maxlen=window_size)
        self._prev_time = time.time()

    def tick(self) -> float:
        """Record a frame tick and return smoothed FPS.

        Call this once per frame.

        Returns:
            Smoothed FPS value.
        """
        curr_time = time.time()
        delta = curr_time - self._prev_time
        if delta > 0:
            self._history.append(1.0 / delta)
        self._prev_time = curr_time
        return self.fps

    @property
    def fps(self) -> float:
        """Get current smoothed FPS value."""
        if not self._history:
            return 0.0
        return sum(self._history) / len(self._history)
