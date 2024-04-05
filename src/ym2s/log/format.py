import logging

from colorama import Fore


class ColoredFormatter(logging.Formatter):
    FORMAT = "%(message)s"

    FORMATS = {
        logging.DEBUG: Fore.WHITE + FORMAT + Fore.RESET,
        logging.INFO: Fore.LIGHTWHITE_EX + FORMAT + Fore.RESET,
        logging.WARNING: Fore.LIGHTYELLOW_EX + FORMAT + Fore.RESET,
        logging.ERROR: Fore.RED + FORMAT + Fore.RESET,
        logging.CRITICAL: Fore.LIGHTRED_EX + FORMAT + Fore.RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
