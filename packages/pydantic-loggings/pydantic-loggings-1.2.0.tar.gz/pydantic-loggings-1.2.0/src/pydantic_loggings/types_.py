import typing as t

from pydantic import RootModel


FormatterStylesType = t.Literal['%', '{', '$']


class StrList(RootModel[list[str]]):
    ...


StrListType = t.Union[StrList, list[str]]
