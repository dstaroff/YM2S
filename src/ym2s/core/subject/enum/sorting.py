"""Enum of subject sorting order."""

from __future__ import annotations

from enum import Enum


class SubjectSortBy(str, Enum):
    """Subject sorting order."""

    Latest = 'latest'
    Oldest = 'oldest'
    LexicalAsc = 'lexical'
    LexicalDesc = 'lexical-desc'

    def __str__(self) -> str:
        return self.value


SORT_BY_VARIANTS: tuple[SubjectSortBy, ...] = (
    SubjectSortBy.Latest,
    SubjectSortBy.Oldest,
    SubjectSortBy.LexicalAsc,
    SubjectSortBy.LexicalDesc,
)
