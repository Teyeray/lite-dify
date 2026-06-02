from __future__ import annotations

from app.domain.entities import AppDefinition, Message, MessageRole, TraceStep, WorkflowNodeType
from app.runtime.llm import ModelGateway


class WorkflowRuntime:
    def __init__(self, model_gateway: ModelGateway) -> None:
        self._model_gateway = model_gateway

    async def run(self, app: AppDefinition, messages: list[Message]) -> tuple[str, list[TraceStep]]:
        answer = ""
        trace: list[TraceStep] = []
        current_input = messages[-1].content if messages else ""

        for node in app.workflow.nodes:
            if node.type == WorkflowNodeType.START:
                trace.append(
                    TraceStep(
                        node_id=node.id,
                        node_type=node.type,
                        status="success",
                        input=current_input,
                        output=current_input,
                    )
                )
            elif node.type == WorkflowNodeType.LLM:
                prompt = node.config.get("prompt", app.system_prompt)
                llm_messages = messages
                if prompt:
                    llm_messages = [
                        Message(conversation_id=messages[-1].conversation_id, role=MessageRole.SYSTEM, content=prompt),
                        *messages,
                    ]
                answer = await self._model_gateway.complete(llm_messages, app.model)
                trace.append(
                    TraceStep(
                        node_id=node.id,
                        node_type=node.type,
                        status="success",
                        input=current_input,
                        output=answer,
                    )
                )
                current_input = answer
            elif node.type == WorkflowNodeType.ANSWER:
                answer = node.config.get("template", current_input)
                trace.append(
                    TraceStep(
                        node_id=node.id,
                        node_type=node.type,
                        status="success",
                        input=current_input,
                        output=answer,
                    )
                )

        if not answer:
            answer = await self._model_gateway.complete(messages, app.model)
        return answer, trace

