import typing as t

from pydantic import Field

from .. import not_set
from ..types_ import StrList
from .handlers import Handler
from .loggers import Logger


class Logging(not_set.Logging):
    handlers: t.Optional[dict[str, Handler]] = Field(default_factory=Handler.default)
    loggers: t.Optional[dict[str, Logger]] = None
    root: t.Optional[Logger] = Logger(handlers=StrList(root=[Handler.NAME]))
