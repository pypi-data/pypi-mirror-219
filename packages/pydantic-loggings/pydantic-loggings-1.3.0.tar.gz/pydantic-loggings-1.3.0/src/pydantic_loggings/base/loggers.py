import logging
import typing as t

from .. import not_set
from .. import utils


class Logger(not_set.Logger):
    level: t.Optional[str] = utils.get_level_name(logging.DEBUG)
