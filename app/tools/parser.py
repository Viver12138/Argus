import json
from dataclasses import dataclass
from typing import Any
from types import SimpleNamespace


@dataclass
class ParsedToolCall:
    tool_call_id: str
    name: str
    arguments: dict[str, Any]

def parse_tool_calls(
        tool_calls: list[Any] | None
) -> list[ParsedToolCall]:

    if not tool_calls:
        return []

    parsed_calls = []

    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        function = tool_call.function

        if not tool_call.id:
            raise ValueError("Tool_call ID is missing")

        if not function.name:
            raise ValueError("Tool name is missing")

        try:
            arguments = json.loads(function.arguments)

        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"Invalid JSON arguments for tool: {function.arguments}") from exc

        if not isinstance(arguments, dict):
            raise ValueError(f"Argument for tool '{function.name}' must be a JSON object")

        parsed_calls.append(
            ParsedToolCall(
                tool_call_id=tool_call_id,
                name=function.name,
                arguments=arguments,
            )
        )

    return parsed_calls
