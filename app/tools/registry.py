from collections.abc import Callable
from typing import Any, Dict

from app.tools.calculator import calculate
from app.tools.text_tool import process_text
from app.tools.datetime_tool import get_datetime


class ToolRegistry:
    """manage registered tools"""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")

        self._tools[name] = function

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")

        return self._tools[name]

    def exists(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

def create_default_registry() -> ToolRegistry:
        """create a registry containing all built-in tools"""

        registry = ToolRegistry()

        registry.register("calculate", calculate)
        registry.register("get_datetime", get_datetime)
        registry.register("process_text", process_text)

        return registry