import json
import logging

import inflect
import yaml

from ym2s.model.serialization import SerializationBackend
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

    def dump(self, path: str, backend: SerializationBackend):
        """
        Dumps subjects into file on path using specified serialization backend
        """
        subjects = {}

        if len(self.tracks) > 0:
            self._logger.debug(
                f'Serializing {self._ie.plural_noun("track", len(self.tracks))}'
            )
            subjects['tracks'] = [track.serialize() for track in self.tracks]
        else:
            self._logger.debug('No tracks to serialize')

        self._logger.debug(f'Serializing subjects to {path} with {backend} backend')
        with open(path, mode='w', encoding="utf-8") as file:
            match backend:
                case SerializationBackend.JSON:
                    json.dump(
                        subjects, file, ensure_ascii=False, indent=2, sort_keys=True
                    )
                case SerializationBackend.YAML:
                    yaml.dump(
                        subjects,
                        file,
                        allow_unicode=True,
                        encoding='utf-8',
                        sort_keys=True,
                    )
