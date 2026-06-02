from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AppMode(StrEnum):
    CHATBOT = "chatbot"
    CHATFLOW = "chatflow"
    WORKFLOW = "workflow"
    AGENT = "agent"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class WorkflowNodeType(StrEnum):
    START = "start"
    LLM = "llm"
    ANSWER = "answer"
    HTTP = "http"
    CODE = "code"
    TOOL = "tool"


class WorkflowNode(BaseModel):
    id: str
    type: WorkflowNodeType
    title: str
    config: dict[str, str] = Field(default_factory=dict)


class WorkflowEdge(BaseModel):
    source: str
    target: str


class WorkflowGraph(BaseModel):
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[WorkflowEdge] = Field(default_factory=list)


class AppDefinition(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    mode: AppMode
    description: str = ""
    model: str | None = None
    system_prompt: str = ""
    workflow: WorkflowGraph = Field(default_factory=WorkflowGraph)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Conversation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_id: UUID
    title: str = "New conversation"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TraceStep(BaseModel):
    node_id: str
    node_type: str
    status: Literal["success", "error"]
    input: str
    output: str


class RunResult(BaseModel):
    conversation: Conversation
    answer: Message
    trace: list[TraceStep] = Field(default_factory=list)

