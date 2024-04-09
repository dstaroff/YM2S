from __future__ import annotations

import json
from typing import TYPE_CHECKING

import yaml

from ym2s.model.serialization import SerializationBackend

if TYPE_CHECKING:
    import logging
    from pathlib import Path

    import inflect

    from ym2s.model.track import Track


class ExportedSubjects:
    def __init__(self, ie: inflect.engine, logger: logging.Logger):
        self._ie = ie
        self._logger = logger.getChild('Subjects')

        self._tracks: list[Track] = []

    @property
    def tracks(self) -> list[Track]:
        return self._tracks

    @tracks.setter
    def tracks(self, tracks: list[Track]):
        self._tracks = tracks

    def dump(self, path: Path, backend: SerializationBackend):
        """
        Dumps subjects into file on path using specified serialization backend
        """
        subjects = {}

        if len(self.tracks) > 0:
            self._logger.debug(
                'Serializing %(track_word)s',
                extra={
                    'track_word': self._ie.plural_noun('track', len(self.tracks)),
                },
            )
            subjects['tracks'] = [track.serialize() for track in self.tracks]
        else:
            self._logger.debug('No tracks to serialize')

        self._logger.debug('Serializing subjects to %s with %s backend', path, backend)
        with path.open(mode='w', encoding='utf-8') as file:
            if backend == SerializationBackend.JSON:
                json.dump(subjects, file, ensure_ascii=False, indent=2, sort_keys=True)
            elif backend == SerializationBackend.YAML:
                yaml.dump(subjects, file, allow_unicode=True, encoding='utf-8', sort_keys=True)
