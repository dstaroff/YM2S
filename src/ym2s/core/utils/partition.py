"""Partition of iterable based on predicate."""

from __future__ import annotations

from typing import Callable, Iterable, TypeVar

T = TypeVar('T')


def partition(predicate: Callable[[T], bool], iterable: Iterable[T]) -> tuple[list[T], list[T]]:
    """Make a partition of iterable based on predicate.

    :param predicate: predicate to check items of iterable.
    :param iterable: iterable.
    :return: two lists: items of iterable passed the predicate, items of iterable failed the predicate.
    """
    res: tuple[list[T], list[T]] = [], []

    for item in iterable:
        res[not predicate(item)].append(item)

    return res
