import typing as t

from pydantic import BaseModel
from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo

from ..types_ import StrList
from ..types_ import StrListType


class Logger(
    BaseModel,
):
    level: t.Optional[str] = None
    propagate: t.Optional[bool] = None
    filters: t.Optional[StrListType] = None
    handlers: t.Optional[StrListType] = None

    @field_validator(
        'filters',
        'handlers',
        mode='before',
    )
    def _list_validator(  # ? TODO
        cls,  # noqa: N805
        v,
        info: FieldValidationInfo,
    ):
        if isinstance(v, str):
            v = StrList.model_validate_json(v)
        return v
