"""Enum of subjects available for a sync."""

from __future__ import annotations

from enum import Enum


class SubjectType(str, Enum):
    """Subjects available for a sync."""

    All = 'all'
    Artists = 'artists'
    Albums = 'albums'
    Tracks = 'tracks'
    Playlists = 'playlists'

    def __str__(self) -> str:
        return self.value


SUBJECT_VARIANTS: tuple[SubjectType, ...] = (
    SubjectType.All,
    SubjectType.Artists,
    SubjectType.Albums,
    SubjectType.Tracks,
    SubjectType.Playlists,
)


SUBJECTS_ALL: tuple[SubjectType, ...] = (
    SubjectType.Artists,
    SubjectType.Albums,
    SubjectType.Tracks,
    SubjectType.Playlists,
)
