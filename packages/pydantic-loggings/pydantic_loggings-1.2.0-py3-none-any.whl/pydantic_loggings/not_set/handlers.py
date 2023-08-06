import typing as t

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo

from .. import mixins
from ..types_ import StrList
from ..types_ import StrListType


class Handler(
    mixins.NameMixin,
    BaseModel,
):
    model_config = ConfigDict(
        populate_by_name=True,
        extra='allow',
    )
    class_: str = Field(alias='()')  # ! both class and ()
    level: t.Optional[str] = None
    formatter: t.Optional[str] = None
    filters: t.Optional[StrListType] = None

    @field_validator(
        'filters',
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
