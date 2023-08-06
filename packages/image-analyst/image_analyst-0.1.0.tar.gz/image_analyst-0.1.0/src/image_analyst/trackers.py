from __future__ import annotations
from image_analyst.models import Detection, DetectionFunction
from image_analyst.utils import iou
from typing import Protocol, NamedTuple, Generator
from dataclasses import dataclass
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass(init=True, repr=True, eq=True, frozen=True)
class ODInstance(Detection):
    """This type represents an object detection instance."""

    id: int


class TrackingFunction(Protocol):
    """This protocol represents a tracking function."""

    def __call__(self, image: np.ndarray) -> list[ODInstance]:
        """Detects the instances in an image.

        Args:
            image (np.ndarray): the image. It must be a valid numpy image.

        Raises:
            InvalidImageException: if `image` is not a valid numpy image.
            InvalidDtypeException: if the image dtype is not supported.
            DetectionFailedException: if the detection has failed.
            TrackingFailedException: if the tracking has failed.

        Returns:
            list[ODInstance]: the instances in the image.
        """
        ...


class TrackingFunctionGenerator(Protocol):
    """This protocol represents a tracking function generator."""

    def __call__(
        self, detection_function: DetectionFunction
    ) -> Generator[TrackingFunction, None, None]:
        """Generates the functions that allows to track the instances in an image.

        Args:
            detection_function (DetectionFunction): the detection function that
                computes the bounding boxes in the image.

        Yields:
            Generator[TrackingFunction, None, None]: the tracking functions.
        """
        ...


class DetectionScore(NamedTuple):
    """This type represents a detection score."""

    detection: Detection
    score: float


class IOUTracker(TrackingFunctionGenerator):
    """This type represents a tracking function generator.

    It uses Intersection Over Union (IOU) to track the instances.
    """

    def __init__(self, iou_threshold: float = 0.25) -> None:
        """Initialises `self` to a new IOUTracker.

        Args:
            iou_threshold (float, optional): the iou threshold. Defaults to 0.25.

        Raises:
            ValueError: if `iou_threshold` is not between 0 and 1.
        """
        if iou_threshold < 0 or iou_threshold > 1:
            raise ValueError("iou_threshold must be between 0 and 1.")

        self.__iou_threshold = iou_threshold

    def create_iou_scores(
        self, detections: list[Detection], previous_instances: list[ODInstance]
    ) -> dict[ODInstance, DetectionScore]:
        """Creates the IOU scores between the detections and the previous instances.

        Args:
            detections (list[Detection]): the detections.
            previous_instances (list[ODInstance]): the previous instances.

        Returns:
            dict[ODInstance, DetectionScore]: the IOU scores.
        """
        iou_scores: dict[ODInstance, DetectionScore] = {}

        for detection in detections:
            best_score = -1
            best_instance = None

            for instance in previous_instances:
                if detection.class_name != instance.class_name:
                    continue

                iou_score = iou(detection.bounding_box, instance.bounding_box)

                if iou_score < self.__iou_threshold:
                    continue

                detection_score = iou_scores.get(instance)

                if detection_score is not None and detection_score.score >= iou_score:
                    continue

                if iou_score <= best_score:
                    continue

                best_score = iou_score
                best_instance = instance

            if best_instance is None:
                continue

            iou_scores[best_instance] = DetectionScore(detection, best_score)

        return iou_scores

    def __call__(  # noqa: D102
        self, detection_function: DetectionFunction
    ) -> Generator[TrackingFunction, None, None]:
        id = 0
        previous_instances = []

        while True:

            def tracking_function(image: np.ndarray) -> list[ODInstance]:
                nonlocal id, previous_instances

                logger.info("Started Bounding boxes creation")
                detections = detection_function(image)
                logger.info("Completed Bounding boxes creation")

                instances: list[ODInstance] = []

                if len(previous_instances) > 0 and len(detections) > 0:
                    logger.info(
                        "Computing IOU between detections and previous detections"
                    )
                    iou_scores = self.create_iou_scores(detections, previous_instances)
                    logger.info("Completed IOU computation")

                    logger.info("Started Instances tracking")
                    for previous_instance, detection_score in iou_scores.items():
                        instances.append(
                            ODInstance(
                                id=previous_instance.id,
                                class_name=detection_score.detection.class_name,
                                score=detection_score.detection.score,
                                bounding_box=detection_score.detection.bounding_box,
                            )
                        )
                        detections.remove(detection_score.detection)
                    logger.info("Completed Instances tracking")

                logger.info("Started new Instances creation")
                for detection in detections:
                    instances.append(
                        ODInstance(
                            id=id,
                            class_name=detection.class_name,
                            score=detection.score,
                            bounding_box=detection.bounding_box,
                        )
                    )
                    id += 1
                logger.info("Completed new Instances creation")

                previous_instances = instances.copy()

                return instances

            yield tracking_function
