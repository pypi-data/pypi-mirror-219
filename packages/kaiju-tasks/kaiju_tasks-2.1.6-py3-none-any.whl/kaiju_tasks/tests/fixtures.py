import pytest  # noqa: pycharm

from kaiju_tasks.services import *
from kaiju_tasks.gui import TaskGUI

__all__ = ['task_service', 'notification_service', 'mock_task_executor', 'task_manager', 'task_gui']


@pytest.fixture
def task_service(app, rpc, database_service) -> TaskService:
    rpc._use_annotation_parser = False
    service = TaskService(app=app, database_service=database_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def notification_service(app, database_service, task_service) -> NotificationService:
    service = NotificationService(app=app, database_service=database_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def mock_executor(app, rpc, mock_stream_client, scheduler) -> TaskExecutor:
    service = TaskExecutor(
        app=app,
        manager_app=mock_stream_client.app_name,
        manager_topic=mock_stream_client.topic,
        stream_client=mock_stream_client,
        rpc_service=rpc,
        scheduler=scheduler,
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def mock_task_executor(app, mock_stream_client, scheduler) -> TaskExecutor:
    mock_stream_client.app_name = 'pytest'
    mock_stream_client.topic = 'manager'
    service = TaskExecutor(
        app=app,
        manager_app=mock_stream_client.app_name,
        manager_topic=mock_stream_client.topic,
        stream_client=mock_stream_client,
        scheduler=scheduler,
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def task_manager(app, redis_client, redis_transport, database_service, notification_service, scheduler) -> TaskManager:
    redis_client.app_name = 'pytest'
    redis_client.topic = 'manager'
    service = TaskManager(
        app=app,
        executor_topic=redis_client.topic,
        redis_transport=redis_transport,
        stream_client=redis_client,
        scheduler_service=scheduler,
        database_service=database_service,
        notification_service=notification_service,
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def task_gui(app, task_service):
    service = TaskGUI(app=app, task_service=task_service)
    app.services.add_service(service)
    return service
