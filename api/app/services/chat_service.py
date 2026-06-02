from __future__ import annotations

from uuid import UUID

from app.domain.entities import AppMode, Conversation, Message, MessageRole, RunResult
from app.domain.repositories import AppRepository, ConversationRepository, MessageRepository
from app.runtime.agent import AgentRuntime
from app.runtime.llm import ModelGateway
from app.runtime.workflow import WorkflowRuntime


class ChatService:
    def __init__(
        self,
        apps: AppRepository,
        conversations: ConversationRepository,
        messages: MessageRepository,
        model_gateway: ModelGateway,
        workflow_runtime: WorkflowRuntime,
        agent_runtime: AgentRuntime,
    ) -> None:
        self._apps = apps
        self._conversations = conversations
        self._messages = messages
        self._model_gateway = model_gateway
        self._workflow_runtime = workflow_runtime
        self._agent_runtime = agent_runtime

    async def chat(self, app_id: UUID, query: str, conversation_id: UUID | None = None) -> RunResult:
        app = self._apps.get(app_id)
        if app is None:
            raise ValueError("App not found")

        conversation = self._load_or_create_conversation(app_id, conversation_id)
        user_message = self._messages.save(
            Message(conversation_id=conversation.id, role=MessageRole.USER, content=query)
        )
        history = [*self._messages.list_by_conversation(conversation.id)]

        if app.mode in {AppMode.CHATFLOW, AppMode.WORKFLOW}:
            answer_text, trace = await self._workflow_runtime.run(app, history)
        elif app.mode == AppMode.AGENT:
            answer_text, trace = await self._agent_runtime.run(app, history)
        else:
            answer_text = await self._model_gateway.complete(history, app.model)
            trace = []

        answer = self._messages.save(
            Message(conversation_id=conversation.id, role=MessageRole.ASSISTANT, content=answer_text)
        )
        return RunResult(conversation=conversation, answer=answer, trace=trace)

    def _load_or_create_conversation(
        self, app_id: UUID, conversation_id: UUID | None
    ) -> Conversation:
        if conversation_id:
            conversation = self._conversations.get(conversation_id)
            if conversation is None:
                raise ValueError("Conversation not found")
            return conversation
        return self._conversations.save(Conversation(app_id=app_id))

