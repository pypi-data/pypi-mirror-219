import dataclasses
from typing import Any


@dataclasses.dataclass
class PluginInfo:
    name: str
    version: int
    author: str
    icon: str
    description: str
    license: str
    repository: str
    homepage: str
    export: Any

    @classmethod
    def from_exec_result(cls, plugin_name: str, result: dict):
        return cls(
            name=result.get("__display_name__", plugin_name),
            version=result.get("__version__", 1),
            author=result.get("__author__", ""),
            icon=result.get("__icon__", ""),
            description=result.get("__description__", ""),
            license=result.get("__license__", "UNLICENSED"),
            repository=result.get("__repository__", ""),
            homepage=result.get("__homepage__", ""),
            export=result.get("__export__", None),
        )
