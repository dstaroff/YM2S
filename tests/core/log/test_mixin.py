"""Tests for ym2s.core.log.mixin."""

import logging
from unittest import TestCase

from hamcrest import assert_that, calling, not_, raises

from ym2s.core.log.mixin import LoggableMixin, LoggerNotInitializedError


class LoggableMixinTest(TestCase):
    """Tests for LoggableMixin."""

    @staticmethod
    def test_not_initialized():
        """Test logger must be initialized."""

        class TestClass(LoggableMixin):
            def test_func(self):
                self.logger().info('test')

        assert_that(calling(TestClass.test_func).with_args(TestClass()), raises(LoggerNotInitializedError))

    @staticmethod
    def test_initialized():
        """Test happy path."""

        class TestClass(LoggableMixin):
            def __init__(self):
                self._set_logger(logging.getLogger())

            def test_func(self):
                self.logger().info('test')

        assert_that(calling(TestClass.test_func).with_args(TestClass()), not_(raises(Exception)))
