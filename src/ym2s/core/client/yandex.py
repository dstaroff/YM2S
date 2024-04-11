"""Yandex Music client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import yandex_music as ym

from ym2s.core.log import LoggableMixin, log_operation
from ym2s.core.subject import Track

if TYPE_CHECKING:
    import inflect


class YMClient(LoggableMixin):
    """Yandex Music API client."""

    def __init__(self, token: str, ie: inflect.engine, logger: logging.Logger):
        self._client = ym.Client(token)
        self._ie = ie
        self._set_logger(logger.getChild('Client.YM'))

    @log_operation('Initializing Yandex Music client', logging.DEBUG)
    def init(self) -> None:
        """Initialize client."""
        self._client.init()

    @log_operation('Listing liked tracks')
    def tracks(self) -> list[Track]:
        """Get list of tracks liked by the user."""
        track_metas: list[ym.TrackShort] = self._client.users_likes_tracks().tracks
        self.logger().info(
            'Got %d liked %s',
            len(track_metas),
            self._ie.plural_noun('track', len(track_metas)),
        )

        filtered_track_metas = [track for track in track_metas if track.album_id is None]
        if len(filtered_track_metas) > 0:
            filtered_tracks = self._client.tracks([track.track_id for track in filtered_track_metas])
            filtered_count = len(filtered_tracks)
            self.logger().warning(
                '%d %s %s no album ID: %s',
                len(filtered_track_metas),
                self._ie.plural_noun('track', len(filtered_track_metas)),
                self._ie.plural_verb('have', filtered_count),
                '; '.join([f'{", ".join(track.artistsName())} — {track.title}' for track in filtered_tracks]),
            )

            self.logger().warning(
                'Probably, %s %s uploaded by user',
                self._ie.plural_noun('it', filtered_count),
                self._ie.plural_verb('was', filtered_count),
            )

        tracks: list[Track] = [
            Track(artists=track.artists_name(), title=track.title)
            for track in self._client.tracks(
                [track_meta.track_id for track_meta in track_metas if track_meta.album_id is not None],
            )
        ]
        self.logger().info(
            'Fetched %d %s',
            len(tracks),
            self._ie.plural_noun('track', len(tracks)),
        )

        return tracks
