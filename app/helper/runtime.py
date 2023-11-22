from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from typing import Optional
from uuid import uuid4

from . import *

correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


def _get_request_id():
    correlation_id.set(uuid4().hex)
    return correlation_id.get()


def loadLogging(filePath=accessFile, logname='', level=0, extra=None):
    _logger = logging.getLogger(logname)
    if level:
        _logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(filePath, mode="a", maxBytes=100 * 1024, backupCount=3)
    if extra == None:
        handler.setFormatter(init_formatter)
    else:
        handler.setFormatter(formatter)
    _logger.addHandler(handler)
    if extra != None:
        _logger = logging.LoggerAdapter(_logger, extra=extra)
    return _logger
