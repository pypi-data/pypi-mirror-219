
from ._types import LogLevelDict, LogOnlyLevels, LogLevel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .logger import Logger

__all__ = ['LoggingContext']


class LoggingContext:

    def __init__(self, log_levels: LogLevelDict):
        self.log_levels = log_levels

        self.loggers: list['Logger'] = []

    def get_level_offset(self):
        return len(max(self.log_levels, key=len))

    def get_logger_name_offset(self):
        return 0 if len(self.loggers) == 0 else len(max(self.loggers, key=lambda l: len(l.name)).name)

    def log_level(self, level: LogLevel, context_level: str | int):

        if isinstance(level, LogOnlyLevels):
            if isinstance(context_level, int):
                context_level = self.log_levels.keys()[self.log_levels.values().index(context_level)]

            return level.log_level(context_level)

        elif isinstance(level, str):
            if isinstance(context_level, str):
                context_level = self.log_levels[context_level]

            return self.log_levels[level] <= context_level
        elif isinstance(level, int):
            if isinstance(context_level, str):
                context_level = self.log_levels[context_level]

            return level <= context_level
