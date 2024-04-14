"""Container for subjects being synced."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import yaml

from ym2s.core.serialization import ISerializer, SerializationBackend
from ym2s.core.subject.album import Album
from ym2s.core.subject.artist import Artist
from ym2s.core.subject.enum import SubjectSortBy
from ym2s.core.subject.playlist import Playlist
from ym2s.core.subject.track import Track

if TYPE_CHECKING:
    import logging
    from pathlib import Path

    import inflect


class Subjects:
    """Subjects being synced."""

    def __init__(self, ie: inflect.engine, logger: logging.Logger):
        self._ie = ie
        self._logger = logger.getChild('Subjects')

        self._artists: tuple[Artist, ...] = tuple[Artist, ...]()
        self._albums: tuple[Album, ...] = tuple[Album, ...]()
        self._tracks: tuple[Track, ...] = tuple[Track, ...]()
        self._playlists: tuple[Playlist, ...] = tuple[Playlist, ...]()

    def get_artists(self) -> tuple[Artist, ...]:
        """Get artists."""
        return self._artists

    def set_artists(self, artists: tuple[Artist, ...]) -> None:
        """Set artists."""
        self._artists = artists

    def get_albums(self) -> tuple[Album, ...]:
        """Get albums."""
        return self._albums

    def set_albums(self, albums: tuple[Album, ...]) -> None:
        """Set albums."""
        self._albums = albums

    def get_tracks(self) -> tuple[Track, ...]:
        """Get tracks."""
        return self._tracks

    def set_tracks(self, tracks: tuple[Track, ...]) -> None:
        """Set tracks."""
        self._tracks = tracks

    def get_playlists(self) -> tuple[Playlist, ...]:
        """Get playlists."""
        return self._playlists

    def set_playlists(self, playlists: tuple[Playlist, ...]) -> None:
        """Set playlists."""
        self._playlists = playlists

    def dump(self, path: Path, backend: SerializationBackend, sort_by: SubjectSortBy):
        """Dump subjects into file on path using specified serialization backend."""
        subjects = self._serialize(sort_by)
        self._logger.debug('Serializing subjects to %s with %s backend', path, backend)
        with path.open(mode='w', encoding='utf-8') as file:
            if backend == SerializationBackend.JSON:
                json.dump(subjects, file, ensure_ascii=False, indent=2, sort_keys=True)
            elif backend == SerializationBackend.YAML:
                yaml.dump(subjects, file, allow_unicode=True, encoding='utf-8', sort_keys=True)

    def _serialize(self, sort_by: SubjectSortBy) -> dict[str, Any]:
        subjects: dict[str, Any] = {}

        subjects_to_serialize: dict[str, tuple[ISerializer, ...]] = {
            'artist': self._artists,
            'album': self._albums,
            'track': self._tracks,
            'playlist': self._playlists,
        }
        for subject_name, container in subjects_to_serialize.items():
            subject_word = self._ie.plural_noun(subject_name, len(container))

            if len(container) > 0:
                self._logger.debug('Serializing %s', subject_word)
                sorted_container: list[ISerializer]
                if sort_by == SubjectSortBy.LexicalAsc:
                    sorted_container = sorted(container)
                elif sort_by == SubjectSortBy.LexicalDesc:
                    sorted_container = sorted(container, reverse=True)
                elif sort_by == SubjectSortBy.Latest:
                    sorted_container = list(reversed(container))
                else:
                    sorted_container = list(container)
                subjects[subject_word] = [subject.serialize() for subject in sorted_container]
            else:
                self._logger.debug('No %s to serialize', subject_word)

        return subjects
