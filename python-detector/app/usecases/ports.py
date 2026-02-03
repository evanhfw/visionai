from abc import ABC, abstractmethod

import numpy as np

from app.domain.detection import Detection


class ObjectDetectorPort(ABC):
    """Port interface for object detection adapters."""

    @abstractmethod
    def detect(self, image: np.ndarray) -> list[Detection]:
        """Detect objects in an image.

        Args:
            image: numpy array representing the image (BGR format from OpenCV)

        Returns:
            List of Detection objects found in the image
        """
        pass
