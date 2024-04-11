"""Tests for ym2s.core.log.decorator."""

import logging
from unittest import TestCase

from hamcrest import assert_that, calling, not_, raises

from ym2s.core.log.decorator import FunctionIsNotAMethodError, NotLoggableMixinBasedClassError, log_operation
from ym2s.core.log.mixin import LoggableMixin


class LogOperationTest(TestCase):
    """Tests for log_operation."""

    @staticmethod
    def test_bare_function():
        """Test decorated function must be the method."""

        @log_operation('test')
        def test_func():
            pass

        assert_that(calling(test_func).with_args(), raises(FunctionIsNotAMethodError))

    @staticmethod
    def test_static_method():
        """Test decorated function can't be static."""

        class TestClass:
            @staticmethod
            @log_operation('test')
            def test_func():
                pass

        assert_that(calling(TestClass.test_func).with_args(), raises(FunctionIsNotAMethodError))

    @staticmethod
    def test_not_using_mixin():
        """Test class must be mixed in with LoggableMixin."""

        class TestClass:
            @log_operation('test')
            def test_func(self):
                pass

        assert_that(calling(TestClass.test_func).with_args(TestClass()), raises(NotLoggableMixinBasedClassError))

    @staticmethod
    def test_using_mixin():
        """Test happy path."""

        class TestClass(LoggableMixin):
            def __init__(self):
                self._set_logger(logging.getLogger())

            @log_operation('test')
            def test_func(self):
                pass

        assert_that(calling(TestClass.test_func).with_args(TestClass()), not_(raises(Exception)))
