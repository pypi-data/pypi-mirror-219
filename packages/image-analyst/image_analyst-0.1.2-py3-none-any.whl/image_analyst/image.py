from image_analyst.exceptions import (
    InvalidImageException,
    InvalidDimensionsException,
)
from dataclasses import dataclass
from typing import Protocol
from enum import Enum, auto
import numpy as np
import math


class ImageFormat(Enum):
    """This type represents an image format."""

    RGB = auto()
    BGR = auto()


@dataclass(init=True, repr=True, eq=True, frozen=True)
class BoundingBox:
    """This type represents a bounding box."""

    xmin: int
    ymin: int
    xmax: int
    ymax: int

    @property
    def center(self) -> tuple[int, int]:
        """Gets the center of the bounding box.

        Returns:
            tuple[int, int]: the center (x, y).
        """
        return (self.xmin + self.width // 2, self.ymin + self.height // 2)

    @property
    def width(self) -> int:
        """Gets the width of the bounding box.

        Returns:
            int: the width.
        """
        return self.xmax - self.xmin + 1

    @property
    def height(self) -> int:
        """Gets the height of the bounding box.

        Returns:
            int: the height.
        """
        return self.ymax - self.ymin + 1

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Gets the bounding box as a tuple.

        Returns:
            tuple[int, int, int, int]: the bounding box
                as a tuple (xmin, ymin, xmax, ymax).
        """
        return (self.xmin, self.ymin, self.xmax, self.ymax)

    def as_box(self) -> tuple[int, int, int, int]:
        """Gets the bounding box as a box.

        Returns:
            tuple[int, int, int, int]: the bounding box
                as a box (x, y, width, height).
        """
        return (self.xmin, self.ymin, self.width, self.height)

    def __post_init__(self) -> None:
        """Checks the init arguments."""
        assert (
            self.xmax >= self.xmin and self.ymax >= self.ymin
        ), "xmax must be greater than xmin and ymax must be greater than ymin."


def verify_image(image: np.ndarray) -> None:
    """Verifies that `image` is a valid numpy image.

    Args:
        image (np.ndarray): the image to verify.

    Raises:
        InvalidImageException: if `image` is not a valid numpy image.
    """
    if image.ndim != 3:
        raise InvalidImageException(
            "The image must be a 3D array (height, width, channels)."
        )

    height, width, channels = image.shape

    if height <= 0 or width <= 0 or channels <= 0:
        raise InvalidImageException(
            "The image has an invalid height, width or channel number."
        )


def verify_dimensions(new_width: int, new_height: int) -> None:
    """Verifies that `new_width` and `new_height` are strictly positive.

    Args:
        new_width (int): the new width.
        new_height (int): the new height.

    Raises:
        InvalidDimensionsException: if `new_width` or
            `new_height` are not stricly positive.
    """
    if new_width <= 0 or new_height <= 0:
        raise InvalidDimensionsException(
            "The new width and height must be strictly positive."
        )


class ResizingFunction(Protocol):
    """This type represents a resizing function."""

    def __call__(
        self, image: np.ndarray, new_width: int, new_height: int
    ) -> np.ndarray:
        """Resizes an image to a new size.

        Args:
            image (np.ndarray): the image to resize. It must be a valid numpy image.
            new_width (int): the new width. It must be stricly positive.
            new_height (int): the new height. It must be stricly positive.

        Raises:
            InvalidImageException: if `image` is not a valid numpy image.
            InvalidDimensionsException: if `new_width` or
                `new_height` are not stricly positive.

        Returns:
            np.ndarray: the resized image.
        """
        ...


def nearest_neighbor_resize_python(
    image: np.ndarray, new_width: int, new_height: int
) -> np.ndarray:
    """Resizes an image to a new size using nearest neighbor interpolation.

    Args:
        image (np.ndarray): the image to resize. It must be a valid numpy image.
        new_width (int): the new width. It must be stricly positive.
        new_height (int): the new height. It must be stricly positive.

    Raises:
        InvalidImageException: if `image` is not a valid numpy image.
        InvalidDimensionsException: if `new_width` or
            `new_height` are not stricly positive.

    Returns:
        np.ndarray: the resized image.
    """
    verify_dimensions(new_width, new_height)
    verify_image(image)

    height, width, channels = image.shape

    if new_width == width and new_height == height:
        return image.copy()

    scale_x = new_width / width
    scale_y = new_height / height

    new_image = np.zeros((new_height, new_width, channels), dtype=image.dtype)

    for y in range(new_height):
        for x in range(new_width):
            nearest_image_x = min(round(x / scale_x), width - 1)
            nearest_image_y = min(round(y / scale_y), height - 1)
            new_image[y, x] = image[nearest_image_y, nearest_image_x]

    return new_image


def bilinear_resize_python(
    image: np.ndarray, new_width: int, new_height: int
) -> np.ndarray:
    """Resizes an image to a new size using bilinear interpolation.

    Args:
        image (np.ndarray): the image to resize. It must be a valid numpy image.
        new_width (int): the new width. It must be stricly positive.
        new_height (int): the new height. It must be stricly positive.

    Raises:
        InvalidImageException: if `image` is not a valid numpy image.
        InvalidDimensionsException: if `new_width` or
            `new_height` are not stricly positive.

    Returns:
        np.ndarray: the resized image.
    """
    verify_dimensions(new_width, new_height)
    verify_image(image)

    height, width, channels = image.shape

    if new_width == width and new_height == height:
        return image.copy()

    scale_x = new_width / width
    scale_y = new_height / height

    new_image = np.zeros((new_height, new_width, channels), dtype=image.dtype)

    for y in range(new_height):
        for x in range(new_width):
            image_x = x / scale_x
            image_y = y / scale_y

            image_xmin = max(math.floor(image_x), 0)
            image_ymin = max(math.floor(image_y), 0)
            image_xmax = min(math.ceil(image_x), width - 1)
            image_ymax = min(math.ceil(image_y), height - 1)

            pixel_xmin_ymin = image[image_ymin, image_xmin]
            pixel_xmax_ymin = image[image_ymin, image_xmax]
            pixel_xmin_ymax = image[image_ymax, image_xmin]
            pixel_xmax_ymax = image[image_ymax, image_xmax]

            if image_xmin == image_xmax and image_ymin == image_ymax:
                new_image[y, x] = pixel_xmin_ymin
            elif image_ymin == image_ymax:
                new_image[y, x] = pixel_xmin_ymin * (
                    image_xmax - image_x
                ) + pixel_xmax_ymin * (image_x - image_xmin)
            elif image_xmin == image_xmax:
                new_image[y, x] = pixel_xmin_ymin * (
                    image_ymax - image_y
                ) + pixel_xmin_ymax * (image_y - image_ymin)
            else:
                x_min_interpolation = pixel_xmin_ymin * (
                    image_xmax - image_x
                ) + pixel_xmax_ymin * (image_x - image_xmin)
                x_max_interpolation = pixel_xmin_ymax * (
                    image_xmax - image_x
                ) + pixel_xmax_ymax * (image_x - image_xmin)
                new_image[y, x] = x_min_interpolation * (
                    image_ymax - image_y
                ) + x_max_interpolation * (image_y - image_ymin)

    return new_image


class EmbeddingFunction(Protocol):
    """This type represents an embedding function."""

    def __call__(
        self, image: np.ndarray, new_width: int, new_height: int
    ) -> tuple[np.ndarray, BoundingBox]:
        """Embeds an image into a black image of the requested size.

        Args:
            image (np.ndarray): the image to embed. It must be a valid numpy image.
            new_width (int): the new width. It must be stricly positive.
            new_height (int): the new height. It must be stricly positive.

        Raises:
            InvalidImageException: if `image` is not a valid numpy image.
            InvalidDimensionsException: if `new_width` or
                `new_height` are not stricly positive.

        Returns:
            tuple[np.ndarray, BoundingBox]: the embedded image and
                the bounding box of the original image.
        """
        ...


class ImageEmbedder(EmbeddingFunction):
    """This class represents an image embedder."""

    def __init__(
        self, resizing_function: ResizingFunction = bilinear_resize_python
    ) -> None:
        """Initialises `self` to a new ImageEmbedder.

        Args:
            resizing_function (ResizingFunction, optional): the resizing function
                to use. Defaults to bilinear_resize_python.
        """
        self.__resizing_function = resizing_function

    def __call__(  # noqa: D102
        self, image: np.ndarray, new_width: int, new_height: int
    ) -> tuple[np.ndarray, BoundingBox]:
        verify_dimensions(new_width, new_height)
        verify_image(image)

        height, width, channels = image.shape

        if new_width == width and new_height == height:
            return (
                image.copy(),
                BoundingBox(xmin=0, ymin=0, xmax=width - 1, ymax=height - 1),
            )

        if new_width / width < new_height / height:
            embedded_height = int((height * new_width) / width)
            embedded_width = new_width
        else:
            embedded_width = int((width * new_height) / height)
            embedded_height = new_height

        ymin = (new_height - embedded_height) // 2
        xmin = (new_width - embedded_width) // 2

        embedded_image = self.__resizing_function(
            image, embedded_width, embedded_height
        )

        result = np.zeros((new_height, new_width, channels), dtype=image.dtype)

        xmax = xmin + embedded_width - 1
        ymax = ymin + embedded_height - 1

        result[ymin : ymax + 1, xmin : xmax + 1, :] = embedded_image

        return result, BoundingBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
