from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.schemas import AppCreateRequest, ChatRequest
from app.domain.entities import AppDefinition, RunResult
from app.infrastructure.container import app_service, chat_service

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/apps")
def list_apps() -> list[AppDefinition]:
    return app_service.list_apps()


@router.post("/apps")
def create_app(payload: AppCreateRequest) -> AppDefinition:
    return app_service.create_app(AppDefinition(**payload.model_dump()))


@router.get("/apps/{app_id}")
def get_app(app_id: UUID) -> AppDefinition:
    try:
        return app_service.get_app(app_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/apps/{app_id}/chat")
async def chat(app_id: UUID, payload: ChatRequest) -> RunResult:
    try:
        return await chat_service.chat(app_id, payload.query, payload.conversation_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

