from __future__ import annotations

import httpx

from app.core.config import settings
from app.domain.entities import Message


class ModelGateway:
    async def complete(self, messages: list[Message], model: str | None = None) -> str:
        if not settings.openai_api_key:
            last_user_message = next((m.content for m in reversed(messages) if m.role == "user"), "")
            return f"Mock response: {last_user_message}"

        payload = {
            "model": model or settings.openai_model,
            "messages": [{"role": message.role, "content": message.content} for message in messages],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(base_url=settings.openai_base_url, timeout=60) as client:
            response = await client.post(
                "/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

