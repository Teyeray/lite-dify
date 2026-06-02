from __future__ import annotations

from uuid import UUID

from app.domain.entities import AppDefinition
from app.domain.repositories import AppRepository


class AppService:
    def __init__(self, apps: AppRepository) -> None:
        self._apps = apps

    def list_apps(self) -> list[AppDefinition]:
        return self._apps.list()

    def get_app(self, app_id: UUID) -> AppDefinition:
        app = self._apps.get(app_id)
        if app is None:
            raise ValueError("App not found")
        return app

    def create_app(self, app: AppDefinition) -> AppDefinition:
        return self._apps.save(app)

