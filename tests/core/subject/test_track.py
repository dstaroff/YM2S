"""Tests for ym2s.core.subject.track."""

from typing import ClassVar
from unittest import TestCase

from hamcrest import assert_that, equal_to
from mustopt import MustOpt

from ym2s.core.subject import Album, Artist, Track


class TrackTest(TestCase):
    """Tests for Track."""

    track_obj: ClassVar = Track(
        title='a',
        artists=(Artist(name='b', id='1'), Artist(name='c', id='2')),
        album=MustOpt.new(
            Album(
                title='d',
                artists=(Artist(name='e', id='3'), Artist(name='f', id='4')),
                id='5',
            )
        ),
        id='6',
    )
    track_dict: ClassVar = {
        'title': 'a',
        'artists': [{'name': 'b', 'id': '1'}, {'name': 'c', 'id': '2'}],
        'album': {
            'title': 'd',
            'artists': [{'name': 'e', 'id': '3'}, {'name': 'f', 'id': '4'}],
            'id': '5',
        },
        'id': '6',
    }

    track_obj_no_album: ClassVar = Track(
        title='a',
        artists=(Artist(name='b', id='1'), Artist(name='c', id='2')),
        album=MustOpt[Album](),
        id='3',
    )
    track_dict_no_album: ClassVar = {
        'title': 'a',
        'artists': [{'name': 'b', 'id': '1'}, {'name': 'c', 'id': '2'}],
        'id': '3',
    }

    def test_serialize_track(self):
        """Test serialization works."""
        assert_that(self.track_obj.serialize(), equal_to(self.track_dict))

    def test_deserialize_track(self):
        """Test deserialization works."""
        assert_that(
            Track.deserialize(self.track_dict),
            equal_to(self.track_obj),
        )

    def test_serialize_track_no_album(self):
        """Test serialization works."""
        assert_that(self.track_obj_no_album.serialize(), equal_to(self.track_dict_no_album))

    def test_deserialize_track_no_album(self):
        """Test deserialization works."""
        assert_that(
            Track.deserialize(self.track_dict_no_album),
            equal_to(self.track_obj_no_album),
        )
