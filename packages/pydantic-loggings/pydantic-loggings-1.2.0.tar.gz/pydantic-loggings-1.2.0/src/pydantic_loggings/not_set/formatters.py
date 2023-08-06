import typing as t

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from .. import mixins
from ..types_ import FormatterStylesType


class Formatter(
    mixins.NameMixin,
    BaseModel,
):
    model_config = ConfigDict(
        # for class_
        populate_by_name=True,
        extra='allow',
    )
    # https://docs.python.org/3/library/logging.html#logging.Formatter
    # https://docs.python.org/3/library/logging.config.html#user-defined-objects
    format_: t.Optional[str] = Field(default=None, alias='format')
    datefmt: t.Optional[str] = None
    # %Y: Year with century as a decimal number.
    # %y: Year without century as a decimal number [00,99].
    #
    # %m: Month as a decimal number [01,12].z
    # %B: Locale’s full month name.
    # %b: Locale’s abbreviated month name.
    #
    # %A: Locale’s full weekday name.
    # %a: Locale’s abbreviated weekday name.
    # %w: Weekday as a decimal number [0(Sunday),6].
    #
    # %d: Day of the month as a decimal number [01,31].
    #
    # %H: Hour (24-hour clock) as a decimal number [00,23].
    # %M: Minute as a decimal number [00,59].
    # %S: Second as a decimal number [00,61].
    style: t.Optional[FormatterStylesType] = None
    validate_: t.Optional[bool] = Field(default=None, alias='validate')
    class_: t.Optional[str] = Field(default=None, alias='()')  # ! both class and ()
