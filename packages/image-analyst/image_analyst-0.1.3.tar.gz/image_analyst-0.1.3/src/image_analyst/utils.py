from __future__ import annotations
from image_analyst.exceptions import DownloadFailedException
from image_analyst.models import BoundingBox, Detection
from typing import Optional, Protocol
from numbers import Real
import urllib.request
import urllib.error
import numpy as np
import logging
import os


logger = logging.getLogger(__name__)


def sigmoid(x: Real | np.ndarray) -> np.ndarray:
    """Computes the sigmoid of x.

    Args:
        x (Real | np.ndarray): the value x.

    Returns:
        np.ndarray: the sigmoid of x.
    """
    return 1.0 / (1.0 + np.exp(-x))


def iou(box1: BoundingBox, box2: BoundingBox) -> float:
    """Returns the Intersection over Union between 2 bounding boxes.

    Args:
        box1 (BoundingBox): The first bounding box.
        box2 (BoundingBox): The second bounding box.

    Raises:
        ZeroDivisionError: if both `box1` and `box2` have a size of 0.

    Returns:
        float: the Intersection over Union between 2 bounding boxes.
    """
    area1 = (box1.xmax - box1.xmin) * (box1.ymax - box1.ymin)
    area2 = (box2.xmax - box2.xmin) * (box2.ymax - box2.ymin)

    w = max(0, min(box1.xmax, box2.xmax) - max(box1.xmin, box2.xmin))
    h = max(0, min(box1.ymax, box2.ymax) - max(box1.ymin, box2.ymin))

    intersection_area = w * h

    union_area = area1 + area2 - intersection_area

    return intersection_area / union_area


class NmsFunction(Protocol):
    """A Non-maximum Suppression function."""

    def __call__(self, detections: list[Detection]) -> list[Detection]:
        """Computes the Non-maximum Suppression (NMS) between a list of detections.

        Args:
            detections (list[Detection]): a list of detections.

        Raises:
            ValueError: if `nms_threshold` is not between 0 and 1.

        Returns:
            list[Detection]: a list of detections.
        """
        ...


class NmsPython(NmsFunction):
    """A Python implementation of the Non-maximum Suppression (NMS) algorithm."""

    def __init__(self, nms_threshold: float = 0.25) -> None:
        """Initializes `self` to a new NmsPython.

        Args:
            nms_threshold (float, optional): the threshold to use
                for the NMS algorithm. Defaults to 0.25.

        Raises:
            ValueError: if `nms_threshold` is not between 0 and 1.
        """
        if nms_threshold < 0 or nms_threshold > 1:
            raise ValueError("nms_threshold must be between 0 and 1.")

        self.nms_threshold = nms_threshold

    def __call__(self, detections: list[Detection]) -> list[Detection]:  # noqa: D102
        result: list[Detection] = []

        unprocessed_detections = set(detections)
        while unprocessed_detections:
            best_detection = max(unprocessed_detections, key=lambda d: d.score)
            result.append(best_detection)
            unprocessed_detections.remove(best_detection)
            for detection in unprocessed_detections.copy():
                if (
                    iou(best_detection.bounding_box, detection.bounding_box)
                    >= self.nms_threshold
                ):
                    unprocessed_detections.remove(detection)

        return result


class ReportFunction(Protocol):
    """A type that represents a report function."""

    def __call__(self, filename: str, current_size: float, total_size: float) -> None:
        """Reports the progress of a download.

        Args:
            filename (str): the filename of the file being downloaded.
            current_size (float): the current size of the file being downloaded.
            total_size (float): the total size of the file being downloaded.
        """
        ...


def download_file(
    url: str,
    filename: str,
    report_callback: Optional[ReportFunction] = None,
) -> str:
    """Downloads a file from a URL to a path.

    Args:
        url (str): the URL to download from.
        filename (str): the filename to save the file as.
        report_callback (Optional[ReportFunction], optional): the report function
            that is called while downloading the files. Defaults to None.

    Returns:
        str: the path to the downloaded file.
    """
    cache_dir = os.path.join(os.path.expanduser("~"), ".image_analyst")
    filepath = os.path.join(cache_dir, filename)

    if os.path.exists(filepath):
        return filepath

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    try:
        with urllib.request.urlopen(url) as response, open(
            os.path.join(cache_dir, filename), "wb"
        ) as f:
            content_length = response.getheader("content-length")
            if content_length is None:
                f.write(response.read())
            else:
                expected_size = int(content_length) / 1024

                i = 0
                while True:
                    chunk = response.read(1024)
                    if not chunk:
                        break
                    i += 1
                    f.write(chunk)
                    f.flush()

                    if report_callback is not None:
                        report_callback(filename, i, expected_size)

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        raise DownloadFailedException("Failed to download file.") from e

    return filepath
