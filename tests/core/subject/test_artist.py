"""Tests for ym2s.core.subject.track."""

from typing import ClassVar
from unittest import TestCase

from hamcrest import assert_that, equal_to

from ym2s.core.subject import Artist


class ArtistTest(TestCase):
    """Tests for Artist."""

    artist_obj: ClassVar = Artist(name='a', id='1')
    artist_dict: ClassVar = {
        'name': 'a',
        'id': '1',
    }

    def test_serialize_artist(self):
        """Test serialization works."""
        assert_that(self.artist_obj.serialize(), equal_to(self.artist_dict))

    def test_deserialize_artist(self):
        """Test deserialization works."""
        assert_that(
            Artist.deserialize(self.artist_dict),
            equal_to(self.artist_obj),
        )
