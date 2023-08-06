import typing as t

from pydantic import Field

from .. import not_set
from ..types_ import FormatterStylesType


class Formatter(not_set.Formatter):
    NAME: t.ClassVar[str] = 'base'
    format_: t.Optional[str] = Field(
        default='{asctime} {levelname:>7} {message}',
        alias='format',
    )
    datefmt: t.Optional[str] = '%m-%d %H:%M:%S'
    style: t.Optional[FormatterStylesType] = '{'
