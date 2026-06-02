from __future__ import annotations

from app.domain.entities import AppDefinition, Message, TraceStep
from app.runtime.llm import ModelGateway


class AgentRuntime:
    def __init__(self, model_gateway: ModelGateway) -> None:
        self._model_gateway = model_gateway

    async def run(self, app: AppDefinition, messages: list[Message]) -> tuple[str, list[TraceStep]]:
        answer = await self._model_gateway.complete(messages, app.model)
        return answer, [
            TraceStep(
                node_id="agent",
                node_type="agent",
                status="success",
                input=messages[-1].content if messages else "",
                output=answer,
            )
        ]

