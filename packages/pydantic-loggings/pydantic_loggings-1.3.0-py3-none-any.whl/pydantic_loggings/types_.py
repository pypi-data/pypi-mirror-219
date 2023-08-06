import typing as t

from pydantic import BaseModel
from pydantic import RootModel


M = t.TypeVar('M', bound=BaseModel)


OptionalModel = t.Optional[t.Union[M, dict[str, t.Any]]]
OptionalModelDict = t.Optional[dict[str, t.Union[M, dict[str, t.Any]]]]


FormatterStylesType = t.Literal['%', '{', '$']


class StrList(RootModel[list[str]]):
    ...


StrListType = t.Union[StrList, list[str]]
