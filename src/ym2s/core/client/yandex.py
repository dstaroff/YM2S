"""Yandex Music client."""

from __future__ import annotations

import asyncio
from base64 import b64encode
from contextlib import closing
import io
import logging
from typing import TYPE_CHECKING

from PIL import Image
from humanfriendly.terminal.spinners import AutomaticSpinner, Spinner
from mustopt import MustOpt
import yandex_music as ym

from ym2s.core.log import LoggableMixin, log_operation
from ym2s.core.subject import Album, Artist, Playlist, Track
from ym2s.core.utils import partition

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

    @log_operation('Listing liked artists')
    def artists(self) -> tuple[Artist, ...]:
        """Get list of artists liked by the user."""
        likes: list[ym.Like] = self._client.users_likes_artists()
        self.logger().info(
            'Got %d liked %s',
            len(likes),
            self._ie.plural_noun('artist', len(likes)),
        )

        artists: tuple[Artist, ...] = tuple(self._get_artist_from_ym(like.artist) for like in likes)
        self.logger().info(
            'Fetched %d %s',
            len(artists),
            self._ie.plural_noun('artist', len(artists)),
        )

        return artists

    @log_operation('Listing liked albums')
    def albums(self) -> tuple[Album, ...]:
        """Get list of albums liked by the user."""
        likes: list[ym.Like] = self._client.users_likes_albums()
        self.logger().info(
            'Got %d liked %s',
            len(likes),
            self._ie.plural_noun('album', len(likes)),
        )

        albums: tuple[Album, ...] = tuple(self._get_album_from_ym(like.album) for like in likes)
        self.logger().info(
            'Fetched %d %s',
            len(albums),
            self._ie.plural_noun('artist', len(albums)),
        )

        return albums

    @log_operation('Listing liked tracks')
    def tracks(self) -> tuple[Track, ...]:
        """Get list of tracks liked by the user."""
        track_metas: list[ym.TrackShort] = self._client.users_likes_tracks().tracks
        self.logger().info(
            'Got %d liked %s',
            len(track_metas),
            self._ie.plural_noun('track', len(track_metas)),
        )

        filtered_tracks, rest_tracks = partition(lambda track_meta: track_meta.album_id is not None, track_metas)
        self._warn_filtered_tracks([track_meta.track_id for track_meta in rest_tracks])

        tracks: tuple[Track, ...] = tuple(
            self._get_track_from_ym(track) for track in self._fetch_tracks(filtered_tracks)
        )

        return tracks

    @log_operation('Listing playlists')
    def playlists(self) -> tuple[Playlist, ...]:
        """Get list of playlists of the user."""
        playlist_metas: list[ym.Playlist] = self._client.users_playlists_list()
        self.logger().info(
            'Got %d %s',
            len(playlist_metas),
            self._ie.plural_noun('playlist', len(playlist_metas)),
        )

        playlist_covers: dict[int, bytes] = self._get_playlist_covers(playlist_metas)

        playlists: list[Playlist] = []
        for pl in playlist_metas:
            cover: MustOpt[bytes] = (
                MustOpt.new(self._encode_playlist_cover_to_base64(playlist_covers[pl.kind]))
                if playlist_covers.get(pl.kind) is not None
                else MustOpt[bytes]()
            )

            self.logger().debug(
                'Fetching %d track meta of playlist "%s" with id %d',
                pl.track_count,
                pl.title,
                pl.kind,
            )
            with AutomaticSpinner(f'Fetching {pl.track_count} track meta of playlist "{pl.title}" with id {pl.kind}'):
                playlist_tracks: list[ym.TrackShort] = pl.fetch_tracks()

            playlists.append(
                self._get_playlist_from_ym(
                    pl,
                    self._fetch_tracks(playlist_tracks) or []
                    if pl.collective
                    else [track.track for track in playlist_tracks],
                    cover,
                ),
            )

        self.logger().info(
            'Fetched %d %s',
            len(playlists),
            self._ie.plural_noun('playlist', len(playlists)),
        )

        return tuple(playlists)

    @classmethod
    def _get_artist_from_ym(cls, artist: ym.Artist) -> Artist:
        return Artist(name=artist.name, id=str(artist.id))

    @classmethod
    def _get_album_from_ym(cls, album: ym.Album) -> Album:
        return Album(
            artists=tuple(cls._get_artist_from_ym(artist) for artist in album.artists),
            title=album.title,
            id=str(album.id),
        )

    @classmethod
    def _get_track_from_ym(cls, track: ym.Track) -> Track:
        return Track(
            artists=tuple(cls._get_artist_from_ym(artist) for artist in track.artists),
            album=next(MustOpt.new(cls._get_album_from_ym(album)) for album in track.albums)
            if len(track.albums) > 0
            else MustOpt[Album](),
            title=track.title,
            id=track.track_id,
        )

    @classmethod
    def _get_playlist_from_ym(cls, playlist: ym.Playlist, tracks: list[ym.Track], cover: MustOpt[bytes]) -> Playlist:
        return Playlist(
            title=playlist.title,
            tracks=tuple(cls._get_track_from_ym(track) for track in tracks),
            cover=cover,
            id=str(playlist.kind),
        )

    def _warn_filtered_tracks(self, filtered_track_ids: list[str]) -> None:
        filtered_count = len(filtered_track_ids)
        if filtered_count > 0:
            filtered_tracks = self._client.tracks(filtered_track_ids)
            self.logger().warning(
                '%d %s %s no album ID: %s. Probably, %s %s uploaded by user',
                filtered_count,
                self._ie.plural_noun('track', filtered_count),
                self._ie.plural_verb('have', filtered_count),
                '; '.join([
                    f'[{track.track_id}] {", ".join(track.artistsName())} — {track.title}' for track in filtered_tracks
                ]),
                self._ie.plural_noun('it', filtered_count),
                self._ie.plural_verb('was', filtered_count),
            )

    def _fetch_tracks(self, track_metas: list[ym.TrackShort]) -> list[ym.Track]:
        filtered_tracks, rest_tracks = partition(lambda track_meta: track_meta.album_id is not None, track_metas)
        self._warn_filtered_tracks([track_meta.track_id for track_meta in rest_tracks])

        track_ids: list[str] = [track_meta.track_id for track_meta in filtered_tracks]
        track_count = len(track_ids)
        track_word = self._ie.plural_noun('track', track_count)

        self.logger().debug('Fetching %d %s', track_count, track_word)

        with AutomaticSpinner(f'Fetching {track_count} {track_word}'):
            tracks = self._client.tracks(track_ids)

        self.logger().info('Fetched %d %s', track_count, track_word)

        return tracks

    def _get_playlist_covers(self, playlist_metas: list[ym.Playlist]) -> dict[int, bytes]:
        playlist_covers: dict[int, bytes] = {}

        playlists_with_cover: list[ym.Playlist] = [
            playlist for playlist in playlist_metas if playlist.cover.type == 'pic'
        ]
        if len(playlists_with_cover) > 0:
            self.logger().info(
                '%d %s %s cover picture. Downloading %s',
                len(playlists_with_cover),
                self._ie.plural_noun('playlist', len(playlists_with_cover)),
                self._ie.plural_verb('have', len(playlists_with_cover)),
                self._ie.singular_noun('them', len(playlists_with_cover)),
            )
            with closing(asyncio.get_event_loop()) as loop:
                # inject async client to retrieve playlist covers asynchronously
                async_client = ym.ClientAsync(self._client.token)
                loop.run_until_complete(async_client.init())
                for i in range(len(playlists_with_cover)):
                    playlists_with_cover[i].client = async_client
                    playlists_with_cover[i].cover.client = async_client

                playlist_covers = loop.run_until_complete(self._download_playlist_covers(playlists_with_cover))

            # inject sync client back
            for i in range(len(playlists_with_cover)):
                playlists_with_cover[i].client = self._client
                playlists_with_cover[i].cover.client = self._client

        return playlist_covers

    @staticmethod
    async def _download_playlist_covers(playlists: list[ym.Playlist]) -> dict[int, bytes]:
        """Download playlist covers as bytes.

        :param playlists: list of playlists to download covers for.
        :return: dict of cover images in bytes by playlist id.
        """

        async def download_cover(playlist: ym.Playlist) -> tuple[int, bytes]:
            return playlist.kind, await playlist.cover.download_bytes_async(size='400x400')

        res: dict[int, bytes] = {}
        with Spinner(label='Downloading playlist covers', total=len(playlists)) as spinner:
            for future in asyncio.as_completed([download_cover(playlist) for playlist in playlists]):
                (playlist_id, cover_data) = await future
                res[playlist_id] = cover_data
                spinner.step()
        return res

    @staticmethod
    def _encode_playlist_cover_to_base64(img_data: bytes) -> bytes:
        cover_image: Image.Image = Image.open(io.BytesIO(img_data))
        cover_image_data: io.BytesIO = io.BytesIO()
        cover_image.convert('RGB').save(cover_image_data, format='JPEG')
        return b64encode(cover_image_data.getvalue())
