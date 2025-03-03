import argparse
from typing import Any, List, OrderedDict, Sequence, TypeVar

__all__ = ["ArgumentParser", "YAMLConfigFileParser", "ConfigFileParser"]
_N = TypeVar("_N")

class ConfigFileParser(object):
    def get_syntax_description(self) -> Any: ...
    def parse(self, stream: Any) -> Any: ...
    def serialize(self, items: OrderedDict[Any, Any]) -> Any: ...

class YAMLConfigFileParser(ConfigFileParser):
    def get_syntax_description(self) -> str: ...
    def parse(self, stream: Any) -> OrderedDict[Any, Any]: ...
    def serialize(
        self, items: OrderedDict[Any, Any], default_flow_style: bool = ...
    ) -> Any: ...

class ArgumentParser(argparse.ArgumentParser):
    @property
    def _config_file_parser(self) -> Any: ...
    @property
    def _default_config_files(self) -> List[Any]: ...
    @property
    def _ignore_unknown_config_file_keys(self) -> Any: ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    # There may be a better way of type hinting this without a type: ignore, but mypy gets unhappy pretty much no matter what as the signatures for parse_args doesn't match with its superclass in argparse
    def parse_args(self, args: Sequence[str] | None = None, namespace: Namespace | None = None, config_file_contents: str | None = None, env_vars: Any = None) -> Namespace: ...  # type: ignore[override]
    def parse_known_args(self, args: Sequence[str] | None = ..., namespace: Namespace | None = ..., config_file_contents: Any = ..., env_vars: Any = ..., ignore_help_args: bool | None = ...) -> tuple[Namespace, list[str]]: ...  # type: ignore[override]
    def get_source_to_settings_dict(self) -> OrderedDict[Any, Any]: ...

Namespace = argparse.Namespace
ArgParser = ArgumentParser
SUPPRESS = argparse.SUPPRESS
