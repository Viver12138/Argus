from typing import Any

from app.tools.parser import parse_tool_calls
from app.tools.executor import ToolExecutor

class ToolRunner:
    def __init__(self, executor: ToolExecutor) -> None:
        self.executor = executor

    def run(
            self,
            tool_calls: list[Any] | None
    ) -> list[dict[str, Any]]:

        parsed_calls = parse_tool_calls(tool_calls)

        results = []

        for call in parsed_calls:
            try:
                result = self.executor.execute(
                    name=call.name,
                    arguments=call.arguments
                )

                results.append({
                    "role": "tool",
                    "tool_call_id": call.tool_call_id,
                    "content": str(result)
                })

            except Exception as exc:
                results.append({
                    "role": "tool",
                    "tool_call_id": call.tool_call_id,
                    "content": f"Tool execution failed: {exc}"
                })

        return results