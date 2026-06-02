from __future__ import annotations

from uuid import uuid4

from app.domain.entities import AppDefinition, AppMode, Conversation
from app.infrastructure.redis_store import RedisAppRepository, RedisConversationRepository


class FakeRedis:
    def __init__(self) -> None:
        self._values: dict[str, tuple[str, object]] = {}

    def scan_iter(self, pattern: str):
        prefix = pattern.removesuffix("*")
        for key in sorted(self._values):
            if key.startswith(prefix):
                yield key

    def get(self, key: str) -> str | None:
        stored = self._values.get(key)
        if stored is None:
            return None
        kind, value = stored
        if kind != "string":
            raise TypeError("WRONGTYPE")
        return str(value)

    def set(self, key: str, value: str) -> None:
        self._values[key] = ("string", value)

    def sadd(self, key: str, value: str) -> None:
        kind, current = self._values.get(key, ("set", set()))
        if kind != "set":
            raise TypeError("WRONGTYPE")
        values = set(current)
        values.add(value)
        self._values[key] = ("set", values)


def test_list_apps_ignores_non_app_record_keys() -> None:
    redis = FakeRedis()
    app_repository = RedisAppRepository(redis)  # type: ignore[arg-type]
    conversation_repository = RedisConversationRepository(redis)  # type: ignore[arg-type]
    app = app_repository.save(AppDefinition(name="Smoke", mode=AppMode.CHATBOT))

    conversation_repository.save(Conversation(app_id=app.id))
    redis.sadd(f"apps:{app.id}:conversation_ids", str(uuid4()))

    apps = app_repository.list()

    assert [item.id for item in apps] == [app.id]
