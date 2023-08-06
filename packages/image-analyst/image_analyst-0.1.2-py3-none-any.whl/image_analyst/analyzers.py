from __future__ import annotations
from image_analyst.trackers import ODInstance
from typing import Protocol, TypeVar, Iterable
from dataclasses import dataclass

T_co = TypeVar("T_co", covariant=True)


class Analyzer(Protocol[T_co]):
    def __call__(self, instances_iterable: Iterable[list[ODInstance]]) -> T_co:
        """Analyzes `instances_iterable`.

        Args:
            instances_iterable (Iterable[list[ODInstance]]): an iterable
                of list of instances.

        Raises:
            AnalysisFailedException: if the analysis cannot be done.

        Returns:
            T_co: The result of the analysis.
        """
        ...


def count(instances_iterable: Iterable[list[ODInstance]]) -> dict[str, int]:
    """Counts the number of unique instance per class name in `instances_iterable`.

    Args:
        instances_iterable (Iterable[list[ODInstance]]): an iterable
            of list of instances.

    Returns:
        dict[str, int]: a dictionary with the class names and
            their numbers in `instances_iterable`.
    """
    counted: set[int] = set()
    result: dict[str, int] = {}

    for instances in instances_iterable:
        for instance in instances:
            if instance.id in counted:
                continue

            if instance.class_name not in result:
                result[instance.class_name] = 1
            else:
                result[instance.class_name] += 1

            counted.add(instance.id)

    return result


@dataclass(init=True, repr=True, eq=True, frozen=True)
class InstanceDirection:
    """This type represents the direction of an instance in an interval."""

    start_id: int
    end_id: int
    origin: tuple[int, int]
    target: tuple[int, int]

    def __post_init__(self) -> None:
        """Checks the init arguments."""
        assert self.start_id > self.end_id, "end_id must be greater than start_id."


def compute_directions(
    instances_iterable: Iterable[list[ODInstance]],
) -> dict[int, InstanceDirection]:
    """Computes the directions of the unique instances in `instances_iterable`.

    Args:
        instances_iterable (Iterable[list[ODInstance]]): an iterable
            of list of instances.

    Returns:
        dict[int, InstanceDirection]: a dictionary with the instance ids and
            their directions.
    """
    directions: dict[int, list[int]] = {}

    for i, instances in enumerate(instances_iterable):
        for instance in instances:
            direction = directions.get(instance.id)

            if direction is None:
                directions[instance.id] = [
                    *instance.bounding_box.center,
                    *instance.bounding_box.center,
                    i,
                    i,
                ]
            else:
                x, y = instance.bounding_box.center
                direction[2] = x
                direction[3] = y
                direction[5] = i

    return {
        id: InstanceDirection(
            start_id=start_id, end_id=end_id, origin=(x1, y1), target=(x2, y2)
        )
        for id, (x1, y1, x2, y2, start_id, end_id) in directions.items()
    }
