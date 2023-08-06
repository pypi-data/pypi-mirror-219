from asyncio import Queue, Task
from typing import Any, Dict, List, Tuple, Optional, TypeVar

from aiohttp import ClientSession, TCPConnector

from resotocore.analytics import AnalyticsEventSender
from resotocore.cli.model import CLI
from resotocore.config import ConfigHandler, ConfigOverride
from resotocore.core_config import CoreConfig
from resotocore.db.db_access import DbAccess
from resotocore.graph_manager.graph_manager import GraphManager
from resotocore.infra_apps.package_manager import PackageManager
from resotocore.infra_apps.runtime import Runtime
from resotocore.message_bus import MessageBus
from resotocore.model.db_updater import GraphMerger
from resotocore.model.model_handler import ModelHandler
from resotocore.query.template_expander import TemplateExpander
from resotocore.report import Inspector
from resotocore.service import Service
from resotocore.task.subscribers import SubscriptionHandler
from resotocore.task.task_handler import TaskHandlerService
from resotocore.types import JsonElement
from resotocore.user import UserManagement
from resotocore.web.certificate_handler import CertificateHandler
from resotocore.worker_task_queue import WorkerTaskQueue

T = TypeVar("T")


class ServiceNames:
    config = "config"
    message_bus = "message_bus"
    event_sender = "event_sender"
    db_access = "db_access"
    model_handler = "model_handler"
    task_handler = "task_handler"
    worker_task_queue = "worker_task_queue"
    template_expander = "template_expander"
    forked_tasks = "forked_tasks"
    cli = "cli"
    config_handler = "config_handler"
    cert_handler = "cert_handler"
    inspector = "inspector"
    infra_apps_runtime = "infra_apps_runtime"
    infra_apps_package_manager = "infra_apps_package_manager"
    user_management = "user_management"
    graph_manager = "graph_manager"
    subscription_handler = "subscription_handler"
    graph_merger = "graph_merger"
    config_override = "config_override"
    http_session = "http_session"
    scheduler = "scheduler"
    core_config_handler = "core_config_handler"
    merge_outer_edges_handler = "merge_outer_edges_handler"
    event_emitter_periodic = "event_emitter_periodic"


class Dependencies(Service):
    def __init__(self, **deps: Any) -> None:
        self.lookup: Dict[str, Any] = deps

    def add(self, name: str, service: T) -> "T":
        self.lookup[name] = service
        return service

    def extend(self, **deps: Any) -> "Dependencies":
        self.lookup = {**self.lookup, **deps}
        return self

    @property
    def services(self) -> List[Service]:
        return [v for _, v in self.lookup.items() if isinstance(v, Service)]

    @property
    def config(self) -> CoreConfig:
        return self.lookup[ServiceNames.config]  # type: ignore

    @property
    def message_bus(self) -> MessageBus:
        return self.lookup[ServiceNames.message_bus]  # type:ignore

    @property
    def event_sender(self) -> AnalyticsEventSender:
        return self.lookup[ServiceNames.event_sender]  # type:ignore

    @property
    def db_access(self) -> DbAccess:
        return self.lookup[ServiceNames.db_access]  # type:ignore

    @property
    def model_handler(self) -> ModelHandler:
        return self.lookup[ServiceNames.model_handler]  # type:ignore

    @property
    def task_handler(self) -> TaskHandlerService:
        return self.lookup[ServiceNames.task_handler]  # type:ignore

    @property
    def worker_task_queue(self) -> WorkerTaskQueue:
        return self.lookup[ServiceNames.worker_task_queue]  # type:ignore

    @property
    def template_expander(self) -> TemplateExpander:
        return self.lookup[ServiceNames.template_expander]  # type:ignore

    @property
    def forked_tasks(self) -> Queue[Tuple[Task[JsonElement], str]]:
        return self.lookup[ServiceNames.forked_tasks]  # type:ignore

    @property
    def cli(self) -> CLI:
        return self.lookup[ServiceNames.cli]  # type:ignore

    @property
    def config_handler(self) -> ConfigHandler:
        return self.lookup[ServiceNames.config_handler]  # type:ignore

    @property
    def cert_handler(self) -> CertificateHandler:
        return self.lookup[ServiceNames.cert_handler]  # type:ignore

    @property
    def inspector(self) -> Inspector:
        return self.lookup[ServiceNames.inspector]  # type:ignore

    @property
    def infra_apps_runtime(self) -> Runtime:
        return self.lookup[ServiceNames.infra_apps_runtime]  # type:ignore

    @property
    def infra_apps_package_manager(self) -> PackageManager:
        return self.lookup[ServiceNames.infra_apps_package_manager]  # type:ignore

    @property
    def user_management(self) -> UserManagement:
        return self.lookup[ServiceNames.user_management]  # type:ignore

    @property
    def graph_manager(self) -> GraphManager:
        return self.lookup[ServiceNames.graph_manager]  # type:ignore

    @property
    def subscription_handler(self) -> SubscriptionHandler:
        return self.lookup[ServiceNames.subscription_handler]  # type:ignore

    @property
    def graph_merger(self) -> GraphMerger:
        return self.lookup[ServiceNames.graph_merger]  # type:ignore

    @property
    def config_override(self) -> ConfigOverride:
        return self.lookup[ServiceNames.config_override]  # type:ignore

    @property
    def http_session(self) -> ClientSession:
        session: Optional[ClientSession] = self.lookup.get(ServiceNames.http_session)
        if not session:
            connector = TCPConnector(limit=0, ssl=False, ttl_dns_cache=300)
            session = ClientSession(connector=connector)
            self.lookup[ServiceNames.http_session] = session
        return session

    async def stop(self) -> None:
        if ServiceNames.http_session in self.lookup:
            await self.http_session.close()
