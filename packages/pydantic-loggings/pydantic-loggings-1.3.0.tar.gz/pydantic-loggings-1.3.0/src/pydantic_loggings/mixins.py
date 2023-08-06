import json as json
import typing as t
from collections import ChainMap


class NameMixin:
    NAME: t.ClassVar[str]

    @classmethod
    def default(cls) -> t.Optional[dict[str, t.Any]]:
        return {cls.NAME: cls()}


class ModelDumpMixin:
    ns_model_dump: t.ClassVar = 'dump_kwarg_'

    @property
    def class_dump_kwargs(self):
        dic = {
            str(cls_var).partition(self.ns_model_dump)[2]: getattr(self, cls_var)
            for cls_var in getattr(self, '__class_vars__')
            if str(cls_var).startswith(self.ns_model_dump)
        }
        return dic

    def model_dump(self, **kwargs):
        model_dump = getattr(super(), 'model_dump')
        dic = model_dump(**dict(ChainMap(self.class_dump_kwargs, kwargs)))
        return dic


class ByAliasModelDumpMixin(ModelDumpMixin):
    dump_kwarg_by_alias: t.ClassVar = True


class ExcludeNoneModelDumpMixin(ModelDumpMixin):
    dump_kwarg_exclude_none: t.ClassVar = True


class ModelDumpJsonMixin(ModelDumpMixin):
    ns_model_dump_json: t.ClassVar = 'dump_json_kwarg_'

    @property
    def class_dump_json_kwargs(self):
        dic = {
            cls_var.partition(self.ns_model_dump_json)[2]: getattr(self, cls_var)
            for cls_var in getattr(self, '__class_vars__')
            if cls_var.startswith(self.ns_model_dump_json)
        }
        return dic

    def model_dump_json(self, **kwargs):
        model_dump = getattr(super(), 'model_dump')
        dic = model_dump(**dict(ChainMap(self.class_dump_kwargs, kwargs)))
        json_str = json.dumps(dic, **self.class_dump_json_kwargs)
        return json_str


class DoNotEnsureAsciiModelDumpJsonModel(ModelDumpJsonMixin):
    dump_json_kwarg_ensure_ascii: t.ClassVar = False


class Indent2ModelDumpJsonModel(ModelDumpJsonMixin):
    dump_json_kwarg_indent: t.ClassVar = 2


# TODO: json yaml ; loads / dumps
# class JsonSettingsSource(PydanticBaseSettingsSource):
#     # https://docs.pydantic.dev/dev-v2/usage/pydantic_settings/#adding-sources
#     @classmethod
#     def settings_customise_sources(
#         cls,
#         settings_cls: t.Type[BaseSettings],
#         init_settings: PydanticBaseSettingsSource,
#         env_settings: PydanticBaseSettingsSource,
#         dotenv_settings: PydanticBaseSettingsSource,
#         file_secret_settings: PydanticBaseSettingsSource,
#     ) -> tuple[PydanticBaseSettingsSource, ...]:
#         return (
#             init_settings,
#             cls(settings_cls),
#             env_settings,
#             file_secret_settings,
#         )

#     def get_field_value(
#         self,
#         field: FieldInfo,
#         field_name: str,
#     ) -> tuple[t.Any, str, bool]:
#         encoding = self.config.get('env_file_encoding')
#         file_content_json = json.loads(
#             Path('tests/example_test_config.json').read_text(encoding)
#         )
#         fiel_value = file_content_json.get(field_name)
#         return fiel_value, field_name, False

#     def prepare_field_value(
#         self,
#         field_name: str,
#         field: FieldInfo,
#         value: t.Any,
#         value_is_complex: bool,
#     ) -> t.Any:
#         return value

#     def __call__(self) -> dict[str, t.Any]:
#         d: dict[str, t.Any] = {}

#         for field_name, field in self.settings_cls.model_fields.items():
#             field_value, field_key, value_is_complex = self.get_field_value(
#                 field, field_name
#             )
#             field_value = self.prepare_field_value(
#                 field_name, field, field_value, value_is_complex
#             )
#             if field_value is not None:
#                 d[field_key] = field_value

#         return d
