"""Tests for ym2s.core.subject.track."""

from typing import ClassVar
from unittest import TestCase

from hamcrest import assert_that, equal_to

from ym2s.core.subject import Album, Artist


class AlbumTest(TestCase):
    """Tests for Album."""

    album_obj: ClassVar = Album(
        title='a',
        artists=(Artist(name='b', id='1'), Artist(name='c', id='2')),
        id='3',
    )
    album_dict: ClassVar = {
        'title': 'a',
        'artists': [{'name': 'b', 'id': '1'}, {'name': 'c', 'id': '2'}],
        'id': '3',
    }

    def test_serialize_album(self):
        """Test serialization works."""
        assert_that(self.album_obj.serialize(), equal_to(self.album_dict))

    def test_deserialize_album(self):
        """Test deserialization works."""
        assert_that(
            Album.deserialize(self.album_dict),
            equal_to(self.album_obj),
        )
