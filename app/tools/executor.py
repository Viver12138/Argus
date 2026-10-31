from typing import Any
import inspect
from app.tools.registry import ToolRegistry

class ToolExecutor:
    """Execute registered tools"""
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute(self,name: str, arguments: dict[str, Any]) -> Any:

        if not isinstance(arguments, dict):
            raise TypeError("Tool arguments must be a dictionary")

        tool = self.registry.get(name)

        signature = inspect.signature(tool)

        try:
            signature.bind(**arguments)
        except TypeError as exc:
            raise ValueError(
                f"Invalid arguments for tool: {name}: {exc}",
            )from exc

        return tool(**arguments)