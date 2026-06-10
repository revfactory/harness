import logging
import sys
from logging.handlers import RotatingFileHandler


def init_logging(level=logging.INFO, logfile: str | None = None, max_bytes: int = 0, backup_count: int = 0):
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    logger = logging.getLogger("harness")
    logger.setLevel(level)

    # clear existing handlers
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter(fmt))
    logger.addHandler(ch)

    # optional rotating file handler
    if logfile:
        if max_bytes and max_bytes > 0:
            fh = RotatingFileHandler(logfile, mode="a", maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        else:
            fh = RotatingFileHandler(logfile, mode="a", maxBytes=0, backupCount=0, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(fmt))
        logger.addHandler(fh)

    return logger
