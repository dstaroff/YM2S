"""Operation logging decorator."""

from __future__ import annotations

from functools import wraps
from inspect import getcallargs
from logging import INFO
from typing import TYPE_CHECKING

from ym2s.core.log.mixin import LoggableMixin

if TYPE_CHECKING:
    from logging import Logger
    from typing import Any, Callable


def log_operation(msg: str, level: int = INFO):
    """Log start and stop of an operation run.

    Function must be a method of a class based on LoggableMixin.
    """

    def _log_operation_impl(f: Callable):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logger = _get_logger(f, *args, **kwargs)

            logger.log(level, '%s...', msg)

            try:
                res = f(*args, **kwargs)
            except RuntimeError:
                logger.exception('%s failed', msg)
                raise

            logger.log(level, '%s done', msg)

            return res

        return wrapper

    return _log_operation_impl


def _get_logger(f: Callable, *args: tuple[Any], **kwargs: dict[str, Any]) -> Logger:
    call_args = getcallargs(f, *args, **kwargs)
    if 'self' not in call_args:
        raise FunctionIsNotAMethodError(f.__name__)

    obj: LoggableMixin = call_args['self']
    if not issubclass(obj.__class__, LoggableMixin):
        raise NotLoggableMixinBasedClassError(obj.__class__.__name__)

    return obj.logger()


class FunctionIsNotAMethodError(RuntimeError):
    """Decorated function must be an instance method."""

    def __init__(self, func_name):
        super().__init__(f'Function {func_name} is not a method.')


class NotLoggableMixinBasedClassError(RuntimeError):
    """Decorated function must be an instance method of a class based on LoggableMixin."""

    def __init__(self, cls_name):
        super().__init__(f'Class {cls_name} is not based on LoggableMixin.')
