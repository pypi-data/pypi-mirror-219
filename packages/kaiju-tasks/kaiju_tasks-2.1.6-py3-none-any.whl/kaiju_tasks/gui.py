import abc
from typing import Iterable

from croniter import croniter

from kaiju_tools import ContextableService, PublicInterface, SERVICE_CLASS_REGISTRY
from kaiju_model.fields import StringField, BooleanField, DateTimeField, IntegerField, JSONObjectField
from kaiju_model.grid.constructor import GridConstructor
from kaiju_model.model import BaseModel
from kaiju_tools.exceptions import ValidationError
from kaiju_tasks.services import TaskService

__all__ = ('TaskEditModel', 'TaskGridModel', 'TaskGUI')


def generate_header(fields: Iterable) -> list:
    header = []

    for i in fields:
        header.append({'id': i, 'label_key': f'label.{i}'})
    return header


def cron_validator(app, key: str, value, **__):
    if value and not croniter.is_valid(value):
        raise ValidationError('Invalid cron', data=dict(key=key, value=value, code='ValidationError.invalid_cron'))


class TaskGridModel(BaseModel, abc.ABC):
    """Task GUI model."""

    id = StringField()
    app_name = StringField()
    commands = JSONObjectField()
    kws = JSONObjectField()
    enabled = BooleanField()
    cron = StringField()
    description = StringField()
    status = StringField()
    result = JSONObjectField()
    exit_code = IntegerField()
    error = JSONObjectField()
    next_run = IntegerField()
    queued_at = IntegerField()
    exec_deadline = IntegerField()


class TaskEditModel(BaseModel, abc.ABC):
    """Task GUI model."""

    id = StringField(read_only=True)
    app_name = StringField(read_only=True)
    commands = JSONObjectField()
    kws = JSONObjectField()
    enabled = BooleanField()
    cron = StringField(field_validator=cron_validator)
    max_exec_timeout = IntegerField(negative_value=False)
    max_retries = IntegerField(negative_value=False)
    restart_policy = StringField()
    notify = BooleanField()
    next_task = StringField()
    description = StringField()
    status = StringField(read_only=True)
    result = JSONObjectField(read_only=True)
    exit_code = IntegerField(read_only=True)
    error = JSONObjectField(read_only=True)
    user_id = StringField(read_only=True)
    next_run = IntegerField(negative_value=False)
    queued_at = IntegerField(read_only=True)
    system = BooleanField()
    created = DateTimeField(read_only=True)


class TaskGUI(ContextableService, PublicInterface):
    """Tasks GUI models."""

    grid_model = TaskGridModel
    edit_model = TaskEditModel
    service_name = 'tasks.gui'
    COLUMNS = (
        'id',
        'app_name',
        'commands',
        'kws',
        'enabled',
        'cron',
        'system',
        'max_exec_timeout',
        'max_retries',
        'restart_policy',
        'notify',
        'next_task',
        'description',
        'status',
        'result',
        'user_id',
        'created',
        'next_run',
        'queued_at',
        'exec_deadline',
        'exit_code',
        'error',
    )
    GRID_FIELDS = (
        'id',
        'description',
        'cron',
        'enabled',
        'status',
        'exit_code',
        'result',
        'error',
        'next_run',
        'queued_at',
        'system',
    )

    def __init__(self, app, task_service: TaskService = None, logger=None):
        super().__init__(app=app, logger=logger)
        self._tasks = task_service

    @property
    def routes(self) -> dict:
        return {'get': self.get, 'grid': self.grid, 'update': self.update, 'abort_and_restart': self.reset_task}

    async def init(self):
        self._tasks = self.discover_service(self._tasks, cls=TaskService)

    async def get(self, id, grouping=False, columns=COLUMNS):
        task = await self._tasks.get(id, columns=columns)
        if not grouping:
            return task
        async with self.edit_model(self.app, **task) as model:
            return model.fields

    async def update(self, id, grouping=False, **kws) -> True:
        task = await self.get(id, grouping=grouping)
        task.update(kws)
        async with self.edit_model(self.app, **task) as _:
            await self._tasks.update(id, data=kws, columns=[])
            return True

    async def reset_task(self, id):
        return await self._tasks.reset_task(id)

    async def grid(self, query=None, conditions=None, page=1, per_page=24):
        offset = per_page * (page - 1)
        if conditions is None:
            conditions = {}
        if query:
            conditions['description'] = {'~': query}
        data = await self._tasks.list(
            columns=self.COLUMNS,
            sort=[{'desc': 'queued_at'}, {'desc': 'created'}],
            conditions=conditions,
            offset=offset,
            limit=per_page,
        )
        models = [self.grid_model(self.app, init=False, **i) for i in data['data']]
        pages = data['pages']
        count = data['count']
        async with GridConstructor(
            self.app,
            models=models,
            fields=self.GRID_FIELDS,
        ) as grid:
            return {
                'data': list(grid),
                'fields': self.GRID_FIELDS,
                'header': generate_header(self.GRID_FIELDS),
                'pagination': {
                    'page': page,
                    'pages': pages,
                    'count': count,
                },
                'count': count,
            }


SERVICE_CLASS_REGISTRY.register(TaskGUI)
