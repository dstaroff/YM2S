"""Tests for ym2s.core.subject.playlist."""

from typing import ClassVar
from unittest import TestCase

from hamcrest import assert_that, equal_to
from mustopt import MustOpt

from ym2s.core.subject import Album, Artist, Playlist, Track


class PlaylistTest(TestCase):
    """Tests for Playlist."""

    playlist_obj: ClassVar = Playlist(
        title='a',
        tracks=(
            Track(
                title='b',
                artists=(Artist(name='c', id='1'), Artist(name='d', id='2')),
                album=MustOpt.new(
                    Album(
                        title='e',
                        artists=(Artist(name='f', id='3'), Artist(name='g', id='4')),
                        id='5',
                    )
                ),
                id='6',
            ),
        ),
        cover=MustOpt.new(b'abc'),
        id='7',
    )
    playlist_dict: ClassVar = {
        'title': 'a',
        'tracks': [
            {
                'title': 'b',
                'artists': [{'name': 'c', 'id': '1'}, {'name': 'd', 'id': '2'}],
                'album': {
                    'title': 'e',
                    'artists': [{'name': 'f', 'id': '3'}, {'name': 'g', 'id': '4'}],
                    'id': '5',
                },
                'id': '6',
            },
        ],
        'cover': 'abc',
        'id': '7',
    }

    playlist_obj_no_cover: ClassVar = Playlist(
        title='a',
        tracks=(
            Track(
                title='b',
                artists=(Artist(name='c', id='1'), Artist(name='d', id='2')),
                album=MustOpt.new(
                    Album(
                        title='e',
                        artists=(Artist(name='f', id='3'), Artist(name='g', id='4')),
                        id='5',
                    )
                ),
                id='6',
            ),
        ),
        cover=MustOpt[bytes](),
        id='7',
    )
    playlist_dict_no_cover: ClassVar = {
        'title': 'a',
        'tracks': [
            {
                'title': 'b',
                'artists': [{'name': 'c', 'id': '1'}, {'name': 'd', 'id': '2'}],
                'album': {
                    'title': 'e',
                    'artists': [{'name': 'f', 'id': '3'}, {'name': 'g', 'id': '4'}],
                    'id': '5',
                },
                'id': '6',
            },
        ],
        'id': '7',
    }

    def test_serialize_playlist(self):
        """Test serialization works."""
        assert_that(self.playlist_obj.serialize(), equal_to(self.playlist_dict))

    def test_deserialize_playlist(self):
        """Test deserialization works."""
        assert_that(
            Playlist.deserialize(self.playlist_dict),
            equal_to(self.playlist_obj),
        )

    def test_serialize_playlist_no_cover(self):
        """Test serialization works."""
        assert_that(self.playlist_obj_no_cover.serialize(), equal_to(self.playlist_dict_no_cover))

    def test_deserialize_playlist_no_cover(self):
        """Test deserialization works."""
        assert_that(
            Playlist.deserialize(self.playlist_dict_no_cover),
            equal_to(self.playlist_obj_no_cover),
        )
