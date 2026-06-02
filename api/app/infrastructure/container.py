from __future__ import annotations

from redis import Redis

from app.core.config import settings
from app.infrastructure.redis_store import (
    RedisAppRepository,
    RedisConversationRepository,
    RedisMessageRepository,
)
from app.runtime.agent import AgentRuntime
from app.runtime.llm import ModelGateway
from app.runtime.workflow import WorkflowRuntime
from app.services.app_service import AppService
from app.services.chat_service import ChatService


redis_client: Redis[str] = Redis.from_url(settings.redis_url, decode_responses=True)

app_repository = RedisAppRepository(redis_client)
conversation_repository = RedisConversationRepository(redis_client)
message_repository = RedisMessageRepository(redis_client)

model_gateway = ModelGateway()
workflow_runtime = WorkflowRuntime(model_gateway)
agent_runtime = AgentRuntime(model_gateway)

app_service = AppService(app_repository)
chat_service = ChatService(
    apps=app_repository,
    conversations=conversation_repository,
    messages=message_repository,
    model_gateway=model_gateway,
    workflow_runtime=workflow_runtime,
    agent_runtime=agent_runtime,
)
