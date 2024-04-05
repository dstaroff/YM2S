import logging
from functools import wraps


def log_operation(msg: str, log_level: int = logging.INFO):
    def _log_operation_impl(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            args[0]._logger.log(log_level, f'{msg}...')
            res = f(*args, **kwargs)
            args[0]._logger.log(log_level, f'{msg} done')

            return res

        return wrapper

    return _log_operation_impl
