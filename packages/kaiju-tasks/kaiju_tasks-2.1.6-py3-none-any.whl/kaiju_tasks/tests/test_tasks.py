import asyncio
from datetime import datetime, timedelta
from time import time
from typing import Generator, cast
from uuid import uuid4

import pytest  # noqa: pycharm
import pytest_asyncio

from kaiju_db.tests.test_db import TestSQLService

from kaiju_tasks.types import Task, Notification, TaskStatus, ExecutorTask, TaskCommand, RestartPolicy
from kaiju_tasks.services import TaskService, NotificationService, TaskExecutor
from kaiju_tasks.gui import TaskGUI

__all__ = ['TestTaskService', 'TestNotificationService', 'TestTaskExecutor', 'TestTaskManager', 'TaskGUI']


@pytest.mark.asyncio
@pytest.mark.docker
class TestTaskService(TestSQLService):
    """Test task service."""

    table_names = [TaskService.table.name]

    @pytest.fixture
    def _service(self, task_service):
        return task_service

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            yield Task(
                id=f'pytest.task.{n}',
                commands=[
                    {'method': 'do.echo', 'params': {'data': '[kws.data]'}},
                    {'method': 'do.echo', 'params': {'data': '[0.result]'}},
                ],
                kws={'data': n},
            )

    async def test_task_reset(self, _store, _row):
        _store = cast(TaskService, _store)
        _row = await _store.create(_row)
        _store._validator = lambda o: o
        await _store.update(_row['id'], Task(status=TaskStatus.EXECUTED.value, job_id='job', stage=1))  # running task
        await _store.reset_task(_row['id'])
        task = await _store.get(_row['id'])
        assert task['status'] == TaskStatus.IDLE.value
        assert task['job_id'] != _row['job_id']
        assert task['stage'] == 0
        assert task

    async def test_remove_old_tasks(self, _store, _rows):
        _store = cast(TaskService, _store)
        await _store.m_create(_rows)
        _store._validator = lambda o: o
        ids = [_r['id'] for _r in _rows]
        t = datetime.now() - timedelta(days=7)
        t = t.date()
        await _store.m_update(ids, {'created': t})
        await _store.delete_old_tasks(6)
        assert not await _store.m_exists(ids)


@pytest.mark.asyncio
@pytest.mark.docker
class TestNotificationService(TestSQLService):
    """Test notifications service."""

    table_names = [NotificationService.table.name, TaskService.table.name]

    @pytest.fixture
    def _service(self, task_service, notification_service):
        return notification_service

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            yield Notification(id=uuid4(), message=f'notification.{n}', kws={'data': n})


@pytest.mark.asyncio
@pytest.mark.docker
class TestTaskExecutor:
    """Test task execution."""

    @pytest_asyncio.fixture
    async def _service(self, app, rpc, mock_task_executor, mock_service):
        rpc._enable_permissions = False
        async with app.services:
            yield mock_task_executor

    async def test_executor_suspend(self, _service: TaskExecutor, mock_stream_client):
        await _service._suspend_self()
        stream = next(iter(mock_stream_client._transport._stream.values()))
        reqs = [stream.get_nowait()[0][0] for _ in range(stream.qsize())]
        assert 'taskman.suspend_executor' in reqs

    async def test_task_execution(self, _service: TaskExecutor, mock_stream_client):
        value_1, value_2 = uuid4(), uuid4()
        task = ExecutorTask(
            id=uuid4().hex,
            commands=[
                TaskCommand(method='do.echo', params={'data': value_1}),
                TaskCommand(method='do.echo', params={'data': '[kws.value_2]'}),
                TaskCommand(method='do.echo', params={'data': '[0]'}),
                TaskCommand(method='do.fail'),
                TaskCommand(method='do.echo'),  # this one must not be executed
            ],
            kws={'value_2': value_2},
            result=[],
            stage=0,
            stages=4,
            exec_deadline=int(time() + 1000),
            job_id='123',
        )
        await _service.run_task(task)
        stream = next(iter(mock_stream_client._transport._stream.values()))
        reqs = [stream.get_nowait()[0] for _ in range(stream.qsize())]
        methods = [r[0] for r in reqs if r[0] != 'taskman.ping']
        params = [r[1] for r in reqs if r[0] != 'taskman.ping']
        assert methods == [
            'taskman.execute_stage',
            'taskman.write_stage',
            'taskman.execute_stage',
            'taskman.write_stage',
            'taskman.execute_stage',
            'taskman.write_stage',
            'taskman.execute_stage',
            'taskman.write_stage',
        ]
        assert params[0]['stage'] == params[1]['stage'] == 0
        assert params[2]['stage'] == params[3]['stage'] == 1
        assert params[4]['stage'] == params[5]['stage'] == 2
        assert params[6]['stage'] == params[7]['stage'] == 3
        assert params[1]['result'] == value_1, 'must be from params'
        assert params[3]['result'] == value_2, 'must be from kws'
        assert params[5]['result'] == value_1, 'must be from the first stage result'
        assert params[7]['error'] is True, 'must indicate an error'


@pytest.mark.asyncio
@pytest.mark.docker
class TestTaskManager:
    """Test task execution."""

    @pytest_asyncio.fixture
    async def _service(self, app, rpc, task_manager):
        rpc._enable_permissions = False
        async with app.services:
            yield task_manager

    @pytest.mark.parametrize(
        ['before_queue', 'after_queue'],
        [
            ({'status': TaskStatus.IDLE.value}, {'status': TaskStatus.QUEUED.value}),
            ({'status': TaskStatus.IDLE.value, 'next_run': int(time()) + 1000}, {'status': TaskStatus.IDLE.value}),
            ({'status': TaskStatus.IDLE.value, 'enabled': False}, {'status': TaskStatus.IDLE.value}),
            ({'status': TaskStatus.QUEUED.value, 'queued_at': time() - 1000}, {'status': TaskStatus.FAILED.value}),
            (
                {'status': TaskStatus.SUSPENDED.value, 'stage': 1, 'result': [1], 'queued_at': int(time())},
                {'status': TaskStatus.QUEUED.value, 'stage': 1, 'result': [1]},
            ),
            (
                {'status': TaskStatus.SUSPENDED.value, 'enabled': False, 'queued_at': int(time())},
                {'status': TaskStatus.SUSPENDED.value},
            ),
            ({'status': TaskStatus.FAILED.value}, {'status': TaskStatus.FAILED.value}),
            (
                {
                    'status': TaskStatus.FAILED.value,
                    'max_retries': 3,
                    'stage': 1,
                    'result': [1],
                    'queued_at': int(time()),
                },
                {'status': TaskStatus.QUEUED.value, 'stage': 1, 'result': [1]},
            ),
            (
                {
                    'status': TaskStatus.FAILED.value,
                    'max_retries': 3,
                    'stage': 1,
                    'result': [1],
                    'restart_policy': RestartPolicy.FIRST.value,
                    'queued_at': int(time()),
                },
                {'status': TaskStatus.QUEUED.value, 'stage': 0, 'result': [1]},
            ),
            (
                {'status': TaskStatus.FAILED.value, 'max_retries': 3, 'enabled': False, 'queued_at': int(time())},
                {'status': TaskStatus.FAILED.value},
            ),
            (
                {'status': TaskStatus.FAILED.value, 'max_retries': 3, 'retries': 3, 'queued_at': int(time())},
                {'status': TaskStatus.FAILED.value},
            ),
            (
                {'status': TaskStatus.FAILED.value, 'cron': '* * * * 5', 'queued_at': int(time())},
                {'status': TaskStatus.IDLE.value},
            ),
            ({'status': TaskStatus.FINISHED.value}, {'status': TaskStatus.FINISHED.value}),
            (
                {'status': TaskStatus.FINISHED.value, 'cron': '* * * * 5', 'stage': 1, 'retries': 3, 'result': [1, 2]},
                {'status': TaskStatus.IDLE.value, 'stage': 0, 'retries': 0, 'result': []},
            ),
        ],
        ids=[
            'IDLE',
            'IDLE not ready',
            'IDLE inactive',
            'QUEUED timeout',
            'SUSPENDED',
            'SUSPENDED inactive',
            'FAILED no restarts',
            'FAILED with restart',
            'FAILED with restart from stage 0',
            'FAILED inactive',
            'FAILED no restarts left',
            'FAILED cron',
            'FINISHED',
            'FINISHED cron',
        ],
    )
    async def test_task_management(self, _service, task_service, before_queue, after_queue):
        task_service._validator = lambda o: o
        task = await task_service.create({'commands': [{'method': 'do'}, {'method': 'do.2'}]}, columns=['id'])
        task = await task_service.update(task['id'], before_queue, columns='*')
        await asyncio.sleep(1)
        task_service.logger.info('Task before: %s', task)
        queue = await _service._queue_tasks()
        task_service.logger.info('Queue %s', queue)
        _task = await task_service.get(task['id'])
        task_service.logger.info('Task after: %s', _task)
        task_service.logger.info('Expected: %s', after_queue)
        for key, value in after_queue.items():
            assert _task[key] == value

    async def test_task_flow(self, _service, task_service, notification_service):
        task_service._validator = lambda o: o
        task = await task_service.create({'commands': [{'method': 'do'}], 'notify': True}, columns=['id', 'job_id'])
        await asyncio.sleep(1)
        await _service._queue_tasks()
        task = await task_service.get(task['id'])
        assert task['status'] == TaskStatus.QUEUED.value
        executor_id = uuid4()
        result = str(uuid4())
        await _service.execute_stage(task['id'], executor_id, 0)
        await _service.write_stage(task['id'], executor_id, 0, 1, result, False)
        notifications = await notification_service.list(conditions={'job_id': task['job_id']})
        notifications = notifications['data']
        assert notifications
        notification = notifications[0]
        task = await task_service.get(task['id'])
        assert task['exit_code'] == 0
        assert task['error'] is None
        assert notification['result'] == task['result'] == [result]
        assert notification['task_id'] == task['id']

    async def test_task_chaining(self, _service, task_service):
        task_service._validator = lambda o: o
        next_task = await task_service.create({'commands': [{'method': 'do'}]})
        task = await task_service.create({'commands': [{'method': 'do'}], 'next_task': next_task['id']}, columns='*')
        await task_service.update(next_task['id'], {'status': TaskStatus.FINISHED.value, 'next_run': time() + 10000})
        executor_id = uuid4()
        await task_service.update(
            task['id'], {'status': TaskStatus.EXECUTED.value, 'executor_id': executor_id, 'stage': 0}
        )
        await _service.write_stage(task['id'], executor_id, 0, 1, 'result', False)
        next_task = await task_service.get(next_task['id'])
        assert next_task['status'] == TaskStatus.IDLE.value
        assert next_task['next_run'] <= time()

    async def test_executor_management(self, _service, task_service):
        task_service._validator = lambda o: o
        new_executor = uuid4()
        await _service.ping(new_executor)
        active = await _service.list_active_executors()
        assert str(new_executor).encode('utf-8') in active
        task = await task_service.create({'commands': [{'method': 'do'}]})
        await task_service.update(task['id'], {'executor_id': new_executor, 'status': TaskStatus.EXECUTED.value})
        await _service.suspend_executor(new_executor)
        active = await _service.list_active_executors()
        assert str(new_executor).encode('utf-8') not in active
        task = await task_service.get(task['id'])
        assert task['status'] == TaskStatus.SUSPENDED.value
        assert task['executor_id'] is None


@pytest.mark.asyncio
@pytest.mark.docker
class TestTaskGUI:
    @pytest_asyncio.fixture
    async def _service(self, app, rpc, task_gui):
        rpc._enable_permissions = False
        async with app.services:
            yield task_gui

    async def test_gui(self, task_service, _service: TaskGUI):
        task = next(TestTaskService.get_rows(1))
        await task_service.create(task)
        await _service.update(task['id'], description='test test test')
        data = await _service.get(task['id'])
        _service.logger.debug(data)
        data = await _service.grid()
        _service.logger.debug(data)
