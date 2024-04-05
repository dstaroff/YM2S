import logging

import inflect
import yandex_music as ym

from ym2s.log.decorator import log_operation
from ym2s.model.track import Track


class YMClient:
    def __init__(self, token: str, ie: inflect.engine, logger: logging.Logger):
        self._client = ym.Client(token)
        self._ie = ie
        self._logger = logger.getChild('Client.YM')

    @log_operation('Initializing Yandex Music client', logging.DEBUG)
    def init(self):
        self._client.init()

    @log_operation('Listing liked tracks')
    def tracks(self) -> list[Track]:
        track_metas: list[ym.TrackShort] = self._client.users_likes_tracks().tracks
        self._logger.info(
            f'Got {len(track_metas)} liked {self._ie.plural_noun("track", len(track_metas))}'
        )

        filtered_track_metas = [
            track for track in track_metas if track.album_id is None
        ]
        if len(filtered_track_metas) > 0:
            filtered_tracks = self._client.tracks(
                [track.track_id for track in filtered_track_metas]
            )
            filtered_count = len(filtered_tracks)
            self._logger.warning(
                f'{len(filtered_track_metas)} {self._ie.plural_noun("track", len(filtered_track_metas))} '
                + f'{self._ie.plural_verb("have", filtered_count)} no album ID: ',
            )
            for track in [
                f'  {", ".join(track.artistsName())} — {track.title}'
                for track in filtered_tracks
            ]:
                self._logger.warning(track)

            self._logger.warning(
                'Probably, '
                + f'{self._ie.plural_noun("it", filtered_count)} {self._ie.plural_verb("was", filtered_count)} '
                + 'uploaded by user'
            )

        tracks: list[Track] = [
            Track(artists=track.artists_name(), title=track.title)
            for track in self._client.tracks(
                [
                    track_meta.track_id
                    for track_meta in track_metas
                    if track_meta.album_id is not None
                ]
            )
        ]
        self._logger.info(
            f'Fetched {len(tracks)} {self._ie.plural_noun("track", len(tracks))}'
        )

        return tracks
