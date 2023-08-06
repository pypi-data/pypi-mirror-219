from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from .. import mixins


class Filter(
    mixins.NameMixin,
    BaseModel,
):
    model_config = ConfigDict(
        populate_by_name=True,
        extra='allow',
    )
    # https://stackoverflow.com/questions/21455515/install-filter-on-logging-level-in-python-using-dictconfig
    class_: str = Field(alias='()')  # ! () only
