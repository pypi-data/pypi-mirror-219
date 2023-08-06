"""Data types."""

from enum import Enum
from datetime import datetime
from typing import Optional, TypedDict, List, Union
from uuid import UUID

from kaiju_tools.rpc import RPCRequest

__all__ = ['TaskStatus', 'RestartPolicy', 'Limit', 'TaskCommand', 'Task', 'Notification', 'ExecutorTask']


class TaskCommand(TypedDict, total=False):
    """Task command (similar to RPC request)."""

    method: str
    params: Optional[dict]


class Limit(Enum):
    """Parameter limits and settings."""

    MAX_STAGES = 100  #: max number of stages per task
    MAX_RETRIES = 10  #: max retries per job
    MIN_T = 10  #: (s) minimum acknowledged time interval in all calculations
    DEFAULT_T = 300  #: (s) default timeout
    MAX_T = 3600 * 4  #: (s) maximum allowed timeout for a single task
    PING_INTERVAL = 30  #: (s) executor ping interval


class TaskStatus(Enum):
    """Task status types."""

    IDLE = 'IDLE'  #: initialized in the table
    QUEUED = 'QUEUED'  #: sent to an executor stream
    EXECUTED = 'EXECUTED'  #: accepted by an executor
    FINISHED = 'FINISHED'  #: all stages completed
    FAILED = 'FAILED'  #: error during stage execution
    SUSPENDED = 'SUSPENDED'  #: executor suspended, waiting for re-queuing


class RestartPolicy(Enum):
    """Task restart policy types."""

    CURRENT = 'CURRENT'  #: restart from the current stage
    FIRST = 'FIRST'  #: restart from the first stage


class Task(TypedDict, total=False):
    """Task object."""

    id: str  #: generated / user-defined unique identifier

    # executor instructions

    app_name: str  #: executor type (app.name)
    commands: List[Union[TaskCommand, RPCRequest, List[TaskCommand], List[RPCRequest]]]  #: sequential list of stages
    kws: dict  #: additional kws template arguments

    # manager instructions

    enabled: bool  #: inactive tasks are not processed
    cron: str  #: cron instructions for periodic tasks
    max_exec_timeout: int  #: (s) max allowed execution time in total
    max_retries: int  #: max retries for a failed task (0 for no retries)
    restart_policy: str  #: how the task will be restarted
    notify: bool  #: notify user about status changes
    next_task: Optional[str]  #: next task to run after finishing of this one
    system: bool  #: system task (should never be removed by cleaning jobs)

    # meta

    description: Optional[str]  #: task long description, completely optional
    meta: dict  #: task metadata, unused by the services

    # managed params

    status: str  #: current task status
    result: list  #: task execution result, a list of stage returns
    stage: int  #: current stage being executed (or about to execute)
    stages: int  #: total number of stages
    queued_at: Optional[int]  #: UNIX time last queued
    exec_deadline: Optional[int]  #: UNIX time deadline
    next_run: Optional[int]  #: UNIX time for next run
    user_id: Optional[UUID]  #: user created the task
    executor_id: Optional[UUID]  #: which executor has this task
    job_id: Optional[str]  #: updated for each new run
    retries: int  #: current number of retries
    created: datetime  #: when task record was added to the table
    exit_code: Optional[int]  #: exit (error) code similar to UNIX codes
    error: Optional[dict]  #: error.repr() if there's an error


class ExecutorTask(TypedDict):
    """Task data passed to an executor by the manager."""

    id: str  #: task id
    commands: List[Union[TaskCommand, RPCRequest]]  #: sequential list of commands
    kws: dict  #: additional kws template arguments
    result: list  #: task execution result, a list of stage returns
    stage: int  #: current stage being executed (or about to execute)
    stages: int  #: total number of stages
    exec_deadline: int  #: UNIX time deadline
    job_id: str  #: current job id for this task


class Notification(TypedDict, total=False):
    """Notification object."""

    id: UUID  #: generated
    message: Optional[str]  #: human-readable message or tag
    kws: Optional[dict]  #: format keywords
    created: datetime  #: timestamp
    enabled: bool  #: mark as read
    user_id: Optional[UUID]  #: receiver
    task_id: Optional[str]  #: task id
    job_id: Optional[str]  #: job id
    status: Optional[str]  #: task status
    result: Optional[list]  #: results
    exit_code: Optional[int]  #: 0 for success
    error: Optional[dict]  #: error.repr() if there's an error
