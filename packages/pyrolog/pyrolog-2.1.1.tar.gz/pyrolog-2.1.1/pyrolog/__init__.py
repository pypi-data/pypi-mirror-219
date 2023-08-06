
"""
    Pyrolog. Pretty logging library
    Copyright (C) 2023  ftdot (https://github.com/ftdot)
"""

from . import defaults
from . import _types as types
from . import utils

from ._types import LogOnlyLevels

from .logger import *
from .logging_context import *
from .handlers import *
from .formatters import *
from .version import *
from .colors import *


def get_plain_logger(log_level: types.LogLevel = 'info'):
    return Logger(
        handlers=[
            StdoutHandler(log_level=log_level)
        ]
    )


def get_colored_logger(log_level: types.LogLevel = 'info'):
    return Logger(
        handlers=[
            StdoutHandler(log_level=log_level, formatter=ColoredFormatter())
        ]
    )
