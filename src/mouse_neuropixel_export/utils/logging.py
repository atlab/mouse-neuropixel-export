import logging
import sys
from pathlib import Path
from typing import Optional


class Logger:
    """
    Thin wrapper around logging.Logger with consistent formatting and
    sensible defaults for library and application use.
    """

    DEFAULT_FORMAT = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_file: Optional[Path | str] = None,
        propagate: bool = False,
    ):
        """
        Parameters
        ----------
        name:
            Logger name (usually __name__).
        level:
            Logging level (e.g. logging.INFO).
        log_file:
            Optional path to a log file.
        propagate:
            Whether to propagate records to ancestor loggers.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = propagate

        if self.logger.handlers:
            # Avoid duplicate handlers if re-instantiated
            return

        formatter = logging.Formatter(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATEFMT,
        )

        # Console handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # Optional file handler
        if log_file is not None:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    # Convenience passthroughs
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)
