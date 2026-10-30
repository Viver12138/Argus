import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class DeepSeekClient:

    def __init__(self) -> None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv(
            "DEEPSEEK_BASE_URL",
            "https://api.deepseek.com",
        )
        self.model = os.getenv(
            "DEEPSEEK_MODEL",
            "deepseek-flash",
        )

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY is not configured"
            )

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0,
            max_retries=0,
        )

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """send a msg and return model's response"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        if not answer:
            raise RuntimeError(
                "DeepSeek returned an empty response"
            )
        return answer.strip()

    async def close(self) -> None:
        """close the client"""
        await self.client.close()