from typing import Any

from app.clients.deepseek import DeepSeekClient, ModelResponse
from app.tools.runner import ToolRunner
from app.tools.schemas import TOOL_SCHEMAS

class Agent:

    def __init__(
            self,
            model_client: DeepSeekClient,
            tool_runner: ToolRunner,
    ) -> None:
        self.model_client = model_client
        self.tool_runner = tool_runner

    async def run(
            self,
            messages: list[dict[str, Any]]
    ) -> ModelResponse:

        while True:

            response = await self.model_client.chat(
                messages=messages,
                tools=TOOL_SCHEMAS
            )

            # final response
            if not response.tool_calls:
                return response

            #original llm_tool_call plus tool_result
            assistant_message = response.raw_message.model_dump(exclude_none=True)
            messages.append(assistant_message)
            tool_results = self.tool_runner.run(response.tool_calls)
            messages.extend(tool_results)

