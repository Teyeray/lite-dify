from __future__ import annotations

from uuid import UUID

from redis import Redis

from app.domain.entities import AppDefinition, Conversation, Message
from app.domain.repositories import AppRepository, ConversationRepository, MessageRepository


class RedisAppRepository(AppRepository):
    def __init__(self, client: Redis[str]) -> None:
        self._client = client

    def list(self) -> list[AppDefinition]:
        apps: list[AppDefinition] = []
        for key in self._client.scan_iter("app:*"):
            raw = self._client.get(key)
            if raw:
                apps.append(AppDefinition.model_validate_json(raw))
        return sorted(apps, key=lambda app: app.created_at)

    def get(self, app_id: UUID) -> AppDefinition | None:
        raw = self._client.get(f"app:{app_id}")
        return AppDefinition.model_validate_json(raw) if raw else None

    def save(self, app: AppDefinition) -> AppDefinition:
        self._client.set(f"app:{app.id}", app.model_dump_json())
        return app


class RedisConversationRepository(ConversationRepository):
    def __init__(self, client: Redis[str]) -> None:
        self._client = client

    def get(self, conversation_id: UUID) -> Conversation | None:
        raw = self._client.get(f"conversation:{conversation_id}")
        return Conversation.model_validate_json(raw) if raw else None

    def save(self, conversation: Conversation) -> Conversation:
        self._client.set(f"conversation:{conversation.id}", conversation.model_dump_json())
        self._client.sadd(f"app:{conversation.app_id}:conversations", str(conversation.id))
        return conversation


class RedisMessageRepository(MessageRepository):
    def __init__(self, client: Redis[str]) -> None:
        self._client = client

    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        values = self._client.lrange(f"conversation:{conversation_id}:messages", 0, -1)
        return [Message.model_validate_json(value) for value in values]

    def save(self, message: Message) -> Message:
        self._client.rpush(f"conversation:{message.conversation_id}:messages", message.model_dump_json())
        return message

