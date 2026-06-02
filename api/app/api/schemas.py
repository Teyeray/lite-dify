from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities import AppMode, WorkflowGraph


class AppCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    mode: AppMode
    description: str = ""
    model: str | None = None
    system_prompt: str = ""
    workflow: WorkflowGraph = Field(default_factory=WorkflowGraph)


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    conversation_id: UUID | None = None

