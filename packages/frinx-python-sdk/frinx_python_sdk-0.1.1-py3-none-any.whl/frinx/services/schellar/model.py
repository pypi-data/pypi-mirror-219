from __future__ import annotations

import typing

from pydantic import Field

from frinx.common.graphql.graphql_types import ENUM
from frinx.common.graphql.graphql_types import Input
from frinx.common.graphql.graphql_types import Mutation
from frinx.common.graphql.graphql_types import Payload
from frinx.common.graphql.graphql_types import Query

Boolean: typing.TypeAlias = bool
DateTime: typing.TypeAlias = typing.Any
Float: typing.TypeAlias = float
ID: typing.TypeAlias = str
Int: typing.TypeAlias = int
JSON: typing.TypeAlias = typing.Any
String: typing.TypeAlias = str


class Status(ENUM):
    UNKNOWN = 'UNKNOWN'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    PAUSED = 'PAUSED'
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'
    TIMED_OUT = 'TIMED_OUT'


class CreateScheduleInput(Input):
    name: String
    workflow_name: String = Field(alias='workflowName')
    workflow_version: String = Field(alias='workflowVersion')
    cron_string: String = Field(alias='cronString')
    enabled: typing.Optional[Boolean]
    parallel_runs: typing.Optional[Boolean] = Field(alias='parallelRuns')
    workflow_context: typing.Optional[String] = Field(alias='workflowContext')
    from_date: typing.Optional[DateTime] = Field(alias='fromDate')
    to_date: typing.Optional[DateTime] = Field(alias='toDate')


class SchedulesFilterInput(Input):
    workflow_name: String = Field(alias='workflowName')
    workflow_version: String = Field(alias='workflowVersion')


class UpdateScheduleInput(Input):
    workflow_name: typing.Optional[String] = Field(alias='workflowName')
    workflow_version: typing.Optional[String] = Field(alias='workflowVersion')
    cron_string: typing.Optional[String] = Field(alias='cronString')
    enabled: typing.Optional[Boolean]
    parallel_runs: typing.Optional[Boolean] = Field(alias='parallelRuns')
    workflow_context: typing.Optional[String] = Field(alias='workflowContext')
    from_date: typing.Optional[DateTime] = Field(alias='fromDate')
    to_date: typing.Optional[DateTime] = Field(alias='toDate')


class CreateScheduleMutation(Mutation):
    _name: str = Field('createSchedule', const=True)
    input: CreateScheduleInput
    payload: Schedule


class UpdateScheduleMutation(Mutation):
    _name: str = Field('updateSchedule', const=True)
    name: String
    input: UpdateScheduleInput
    payload: Schedule


class DeleteScheduleMutation(Mutation):
    _name: str = Field('deleteSchedule', const=True)
    name: String
    payload: Boolean


class PageInfo(Payload):
    has_next_page: typing.Optional[Boolean] = Field(response='Boolean', alias='hasNextPage', default=True)
    has_previous_page: typing.Optional[Boolean] = Field(response='Boolean', alias='hasPreviousPage', default=True)
    start_cursor: typing.Optional[Boolean] = Field(response='String', alias='startCursor', default=True)
    end_cursor: typing.Optional[Boolean] = Field(response='String', alias='endCursor', default=True)


class ScheduleQuery(Query):
    _name: str = Field('schedule', const=True)
    name: String
    payload: Schedule


class SchedulesQuery(Query):
    _name: str = Field('schedules', const=True)
    after: typing.Optional[String]
    before: typing.Optional[String]
    first: typing.Optional[Int]
    last: typing.Optional[Int]
    filter: typing.Optional[SchedulesFilterInput]
    payload: ScheduleConnection


class Schedule(Payload):
    name: typing.Optional[Boolean] = Field(response='String', default=True)
    enabled: typing.Optional[Boolean] = Field(response='Boolean', default=True)
    parallel_runs: typing.Optional[Boolean] = Field(response='Boolean', alias='parallelRuns', default=True)
    workflow_name: typing.Optional[Boolean] = Field(response='String', alias='workflowName', default=True)
    workflow_version: typing.Optional[Boolean] = Field(response='String', alias='workflowVersion', default=True)
    cron_string: typing.Optional[Boolean] = Field(response='String', alias='cronString', default=True)
    workflow_context: typing.Optional[Boolean] = Field(response='String', alias='workflowContext', default=True)
    from_date: typing.Optional[Boolean] = Field(response='DateTime', alias='fromDate', default=True)
    to_date: typing.Optional[Boolean] = Field(response='DateTime', alias='toDate', default=True)
    status: typing.Optional[Boolean] = Field(response='Status', default=True)


class ScheduleConnection(Payload):
    edges: typing.Optional[ScheduleEdge] = Field(response='ScheduleEdge')
    page_info: typing.Optional[PageInfo] = Field(response='PageInfo', alias='pageInfo')
    total_count: typing.Optional[Boolean] = Field(response='Int', alias='totalCount', default=True)


class ScheduleEdge(Payload):
    node: typing.Optional[Schedule] = Field(response='Schedule')
    cursor: typing.Optional[Boolean] = Field(response='String', default=True)


CreateScheduleInput.update_forward_refs()
SchedulesFilterInput.update_forward_refs()
UpdateScheduleInput.update_forward_refs()
CreateScheduleMutation.update_forward_refs()
UpdateScheduleMutation.update_forward_refs()
DeleteScheduleMutation.update_forward_refs()
PageInfo.update_forward_refs()
ScheduleQuery.update_forward_refs()
SchedulesQuery.update_forward_refs()
Schedule.update_forward_refs()
ScheduleConnection.update_forward_refs()
ScheduleEdge.update_forward_refs()
