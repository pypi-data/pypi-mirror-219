import logging
import typing as t

from pydantic import Field

from .. import not_set
from .. import utils
from .formatters import Formatter


class Handler(not_set.Handler):
    NAME: t.ClassVar[str] = 'base'
    class_: str = Field(default='logging.StreamHandler', alias='()')
    level: t.Optional[str] = utils.get_level_name(logging.DEBUG)
    formatter: t.Optional[str] = Formatter.NAME
