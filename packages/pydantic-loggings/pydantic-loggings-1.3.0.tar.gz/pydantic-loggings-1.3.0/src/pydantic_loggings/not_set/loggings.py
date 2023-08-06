import json
import logging
import typing as t
from logging.config import DictConfigurator

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .. import mixins
from ..types_ import OptionalModel
from ..types_ import OptionalModelDict
from .filters import Filter
from .formatters import Formatter
from .handlers import Handler
from .loggers import Logger


class Logging(
    mixins.ByAliasModelDumpMixin,
    mixins.ExcludeNoneModelDumpMixin,
    mixins.DoNotEnsureAsciiModelDumpJsonModel,
    mixins.Indent2ModelDumpJsonModel,
    BaseSettings,
):
    model_config = SettingsConfigDict(
        env_prefix='log__',
        env_nested_delimiter='__',
        extra='ignore',
    )
    # https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema
    # https://docs.python.org/3/howto/logging-cookbook.html#an-example-dictionary-based-configuration
    version: int = 1  # ok
    formatters: OptionalModelDict[Formatter] = None
    filters: OptionalModelDict[Filter] = None
    handlers: OptionalModelDict[Handler] = None
    loggers: OptionalModelDict[Logger] = None
    root: OptionalModel[Logger] = None
    incremental: t.Optional[bool] = None
    disable_existing_loggers: t.Optional[bool] = None

    configurator: t.ClassVar = DictConfigurator

    @field_validator(
        'formatters',
        'filters',
        'handlers',
        'loggers',
        mode='before',
    )
    def _dict_validator(  # ? TODO
        cls,  # noqa: N805
        v,
        info: FieldValidationInfo,
    ):
        if isinstance(v, str):
            v = json.loads(v)
        if isinstance(v, dict):
            for name, val in v.items():
                if isinstance(val, str):
                    v[name] = json.loads(val)
        return v

    @property
    def configuration(self):
        return self.model_dump()

    def configure(self):
        self.configurator(self.configuration).configure()

    def get_logger(
        self,
        logger_name: str = '',
        /,
        *,
        level: t.Optional[t.Union[int, str]] = None,
        force_level: bool = False,
        configure: bool = False,
    ):
        if configure:
            self.configure()
        logger = logging.getLogger(name=logger_name)
        if level is not None:
            if force_level:
                logger.setLevel(level=level)
            elif logging.NOTSET == logger.level:
                logger.setLevel(level=level)
            elif logging.NOTSET == logger.getEffectiveLevel():
                logger.setLevel(level=level)
        return logger
