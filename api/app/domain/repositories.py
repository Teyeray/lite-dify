from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import AppDefinition, Conversation, Message


class AppRepository(ABC):
    @abstractmethod
    def list(self) -> list[AppDefinition]:
        raise NotImplementedError

    @abstractmethod
    def get(self, app_id: UUID) -> AppDefinition | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, app: AppDefinition) -> AppDefinition:
        raise NotImplementedError


class ConversationRepository(ABC):
    @abstractmethod
    def get(self, conversation_id: UUID) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError


class MessageRepository(ABC):
    @abstractmethod
    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def save(self, message: Message) -> Message:
        raise NotImplementedError

