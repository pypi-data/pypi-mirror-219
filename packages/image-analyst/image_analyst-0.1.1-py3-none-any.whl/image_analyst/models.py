from image_analyst.image import ImageFormat, BoundingBox
from dataclasses import dataclass
from typing import Protocol
import numpy as np


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Detection:
    """This type represents an object detection."""

    class_name: str
    score: float
    bounding_box: BoundingBox

    def __post_init__(self) -> None:
        """Checks the init arguments."""
        assert 0 <= self.score and self.score <= 1, "The score must be between 0 and 1."


class DetectionFunction(Protocol):
    """This protocol represents an detection function."""

    def __call__(self, image: np.ndarray) -> list[Detection]:
        """Detects the bounding boxes, classes and scores of instances in `image`.

        Args:
            image (np.ndarray): The image. It must be a valid numpy image.

        Raises:
            InvalidImageException: if `image` is not a valid numpy image.
            InvalidDtypeException: if the image dtype is not supported.
            DetectionFailedException: if the detection has failed.

        Returns:
            list[Detection]: The list of detections in `image`.
        """
        ...


class ODModel(DetectionFunction, Protocol):
    """This protocol represents an object detection model."""

    @property
    def supported_classes(self) -> tuple[str, ...]:
        """Gets the supported classes.

        Returns:
            tuple[str, ...]: the supported classes.
        """
        ...

    @property
    def supported_format(self) -> ImageFormat:
        """Gets the supported image format.

        Returns:
            ImageFormat: the supported image format.
        """
        ...

    @property
    def supported_dtype(self) -> type:
        """Gets the supported image dtype.

        Returns:
            type: the supported image dtype.
        """
        ...
