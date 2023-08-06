import typing as t

from .. import not_set


class Filter(not_set.Filter):
    NAME: t.ClassVar[str] = 'base'
