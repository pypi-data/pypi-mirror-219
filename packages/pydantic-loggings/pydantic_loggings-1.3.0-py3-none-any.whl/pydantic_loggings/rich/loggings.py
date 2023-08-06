from pydantic import Field

from .. import not_set
from ..types_ import OptionalModel
from ..types_ import OptionalModelDict
from ..types_ import StrList
from .handlers import Handler
from .loggers import Logger


class Logging(not_set.Logging):
    handlers: OptionalModelDict[Handler] = Field(default_factory=Handler.default)
    loggers: OptionalModelDict[Logger] = None
    root: OptionalModel[Logger] = Logger(handlers=StrList(root=[Handler.NAME]))
