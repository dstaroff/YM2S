"""Tests for ym2s.core.subject.track."""

from typing import ClassVar
from unittest import TestCase

from hamcrest import assert_that, equal_to

from ym2s.core.subject import Track


class TrackTest(TestCase):
    """Tests for Track."""

    track_obj: ClassVar = Track(
        artists=['a', 'b'],
        title='c',
    )
    track_dict: ClassVar = {
        'artists': ['a', 'b'],
        'title': 'c',
    }

    def test_serialize_track(self):
        """Test serialization works."""
        assert_that(self.track_dict, equal_to(self.track_obj.serialize()))

    def test_deserialize_track(self):
        """Test deserialization works."""
        assert_that(
            self.track_obj,
            equal_to(Track.deserialize(self.track_dict)),
        )
