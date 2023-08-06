from enum import Enum
from typing import Any
from typing import Optional
from typing import TypeAlias

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import StrictBool
from pydantic import root_validator
from pydantic import validator
from pydantic.utils import ROOT_KEY

from frinx.common.conductor_enums import DoWhileEvaluatorType
from frinx.common.conductor_enums import SwitchEvaluatorType
from frinx.common.conductor_enums import WorkflowStatus
from frinx.common.util import snake_to_camel_case
from frinx.common.worker.worker import WorkerImpl

WorkflowTask: TypeAlias = dict[str, str]
TaskDef: TypeAlias = dict[str, str]
TaskToDomain: TypeAlias = dict[str, str]
WorkflowDef: TypeAlias = dict[str, Any]
WorkflowImpl: TypeAlias = dict[str, Any]


class TaskType(str, Enum):
    SIMPLE = 'SIMPLE'
    DYNAMIC = 'DYNAMIC'
    FORK_JOIN = 'FORK_JOIN'
    FORK_JOIN_DYNAMIC = 'FORK_JOIN_DYNAMIC'
    DECISION = 'DECISION'
    SWITCH = 'SWITCH'
    JOIN = 'JOIN'
    DO_WHILE = 'DO_WHILE'
    SUB_WORKFLOW = 'SUB_WORKFLOW'
    START_WORKFLOW = 'START_WORKFLOW'
    EVENT = 'EVENT'
    WAIT = 'WAIT'
    HUMAN = 'HUMAN'
    USER_DEFINED = 'USER_DEFINED'
    HTTP = 'HTTP'
    LAMBDA = 'LAMBDA'
    INLINE = 'INLINE'
    EXCLUSIVE_JOIN = 'EXCLUSIVE_JOIN'
    TERMINATE = 'TERMINATE'
    KAFKA_PUBLISH = 'KAFKA_PUBLISH'
    JSON_JQ_TRANSFORM = 'JSON_JQ_TRANSFORM'
    SET_VARIABLE = 'SET_VARIABLE'


class WorkflowTaskImpl(BaseModel):
    # REQUIRED
    name: str
    task_reference_name: str
    # PREDEFINED
    type: TaskType
    start_delay: int = Field(default=0)
    optional: StrictBool = Field(default=False)
    async_complete: StrictBool = Field(default=False)
    default_case: list[WorkflowTask] | list[Any] = Field(default=[])
    input_parameters: Any | dict[str, Any] = Field(default={})

    # OPTIONAL
    description: Optional[str] = Field(default=None)
    dynamic_task_name_param: Optional[str] = Field(default=None)
    case_value_param: Optional[str] = Field(default=None)
    case_expression: Optional[str] = Field(default=None)
    script_expression: Optional[str] = Field(default=None)
    decision_cases: Optional[dict[str, list[WorkflowTask]] | dict[str, list[Any]]] = Field(default=None)
    dynamic_fork_join_tasks_param: Optional[str] = Field(default=None)
    dynamic_fork_tasks_param: Optional[str] = Field(default=None)
    dynamic_fork_tasks_input_param_name: Optional[str] = Field(default=None)
    fork_tasks: Optional[list[list[Any]]] = Field(default=None)
    sub_workflow_param: Optional[Any] = Field(default=None)
    join_on: Optional[list[str]] = Field(default=None)
    sink: Optional[str] = Field(default=None)
    task_definition: Optional[TaskDef] = Field(default=None)
    rate_limited: Optional[StrictBool] = Field(default=None)
    default_exclusive_join_task: Optional[list[str]] = Field(default=None)
    loop_condition: Optional[str] = Field(default=None)
    loop_over: Optional[list[Any]] = Field(default=None)
    retry_count: Optional[int] = Field(default=None)
    evaluator_type: Optional[str] = Field(default=None)
    expression: Optional[str] = Field(default=None)
    workflow_task_type: Optional[str] = Field(default=None)

    class Config:
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        validate_all = True

    def output_ref(self, path: str | None = None) -> str:
        if not path or path is None:
            return f'${{{self.task_reference_name}.output}}'
        return f'${{{self.task_reference_name}.output.{path}}}'


class DoWhileTask(WorkflowTaskImpl):
    type: TaskType = TaskType.DO_WHILE
    loop_condition: str
    loop_over: list[WorkflowTaskImpl]
    evaluator_type: DoWhileEvaluatorType = DoWhileEvaluatorType.JAVASCRIPT


class DynamicForkTaskInputParameters(BaseModel):
    dynamic_tasks: str | object
    dynamic_tasks_input: str | object

    class Config:
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class DynamicForkTaskFromDefInputParameters(BaseModel):
    dynamic_tasks: str | object
    dynamic_tasks_input: str

    class Config:
        validate_assignment = True
        allow_mutation = True
        validate_all = True

    @root_validator(pre=True)
    def check_input_values(cls, values: dict[str, Any]) -> Any:  # noqa: N805
        values['dynamic_tasks'] = values['dynamic_tasks'].__fields__['name'].default
        return values


class DynamicForkArraysTaskFromDefInputParameters(BaseModel):
    fork_task_name: object
    fork_task_inputs: list[dict[object, str]] | None | str = []

    @root_validator(pre=True)
    def check_input_values(cls, values: dict[str, Any]) -> Any:  # noqa: N805
        wf_def_input_params = list(values['fork_task_name'].WorkflowInput.__fields__.keys())
        fork_task_inputs = values['fork_task_inputs']

        for fork_task_input in fork_task_inputs:
            if not bool(set(fork_task_input.keys()) & set(wf_def_input_params)):
                raise ValueError(
                    f"""StartWorkflowTaskFromDefInputParameters bad input fields
                        expected: {wf_def_input_params}
                        inserted: {fork_task_inputs}
                    """
                )

        values['fork_task_name'] = values['fork_task_name'].__fields__['name'].default
        return values

    class Config:
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class DynamicForkArraysTaskInputParameters(BaseModel):
    fork_task_name: str
    fork_task_inputs: list[dict[str, Any]] | str

    class Config:
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class DynamicForkTask(WorkflowTaskImpl):
    # TODO why not render in UI?
    type: TaskType = TaskType.FORK_JOIN_DYNAMIC
    dynamic_fork_tasks_param: str = Field(default='dynamicTasks')
    dynamic_fork_tasks_input_param_name: str = Field(default='dynamicTasksInput')
    input_parameters: DynamicForkArraysTaskInputParameters | DynamicForkTaskInputParameters \
                      | DynamicForkArraysTaskFromDefInputParameters | DynamicForkTaskFromDefInputParameters


class ForkTask(WorkflowTaskImpl):
    type: TaskType = TaskType.FORK_JOIN
    fork_tasks: list[list[WorkflowTaskImpl]]


class HttpMethod(str, Enum):
    GET = ('GET',)
    PUT = ('PUT',)
    POST = ('POST',)
    DELETE = ('DELETE',)
    HEAD = ('HEAD',)
    OPTIONS = 'OPTIONS'


# TODO HTTP TASK?


class HumanTask(WorkflowTaskImpl):
    type: TaskType = TaskType.HUMAN


class InlineTaskInputParameters(BaseModel):
    evaluator_type: str = Field(default='javascript', alias='evaluatorType')
    expression: str

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        extra = Extra.allow

    def __init__(self, expression: str, **data: Any) -> None:
        data['expression'] = expression
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)

    @validator('expression', always=True)
    def expression_in_function(cls, expression: str) -> str:  # noqa: N805
        if not expression.startswith('function'):
            expression = f'function e() {{ {expression} }} e();'
        return expression


class InlineTask(WorkflowTaskImpl):
    type: TaskType = TaskType.INLINE
    input_parameters: InlineTaskInputParameters


class LambdaTaskInputParameters(BaseModel):
    script_expression: str = Field(alias='scriptExpression')

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        extra = Extra.allow

    def __init__(self, script_expression: str, **data: Any) -> None:
        data['script_expression'] = script_expression
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


class LambdaTask(WorkflowTaskImpl):
    type: TaskType = TaskType.LAMBDA
    input_parameters: LambdaTaskInputParameters


class WaitDurationTaskInputParameters(BaseModel):
    duration: str


class WaitDurationTask(WorkflowTaskImpl):
    type: TaskType = TaskType.WAIT
    input_parameters: WaitDurationTaskInputParameters


class WaitUntilTaskInputParameters(BaseModel):
    until: str


class WaitUntilTask(WorkflowTaskImpl):
    type: TaskType = TaskType.WAIT
    input_parameters: WaitUntilTaskInputParameters


class TerminateTaskInputParameters(BaseModel):
    termination_status: WorkflowStatus
    termination_reason: str | None
    workflow_output: dict[str, Any] | str | None

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class TerminateTask(WorkflowTaskImpl):
    type: TaskType = TaskType.TERMINATE
    input_parameters: TerminateTaskInputParameters


class StartWorkflowTaskPlainInputParameters(BaseModel):
    name: str
    version: Optional[int] = Field(default=None)
    input: dict[str, object] | None = {}
    correlation_id: str | None = Field(alias='correlationId')


class StartWorkflowTaskFromDefInputParameters(BaseModel):
    workflow: object
    input: dict[str, object] | None = {}
    correlation_id: str | None = Field(alias='correlationId')

    @root_validator(pre=True)
    def check_input_values(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        wf_def_input = list(values['workflow'].WorkflowInput.__fields__.keys())
        wf_input = list(values['input'].keys())
        if not bool(set(wf_input) & set(wf_def_input)):
            raise ValueError(
                f"""StartWorkflowTaskFromDefInputParameters bad input fields
                    expected: {wf_def_input}
                    inserted: {wf_input}
                """
            )
        values['name'] = values['workflow'].__fields__['name'].default
        values['version'] = values['workflow'].__fields__['version'].default

        return values

    class Config:
        extra = Extra.allow


class StartWorkflowTaskInputParameters(BaseModel):
    start_workflow: StartWorkflowTaskPlainInputParameters | StartWorkflowTaskFromDefInputParameters

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class StartWorkflowTask(WorkflowTaskImpl):
    type: TaskType = TaskType.START_WORKFLOW
    input_parameters: StartWorkflowTaskInputParameters


class SwitchTaskInputParameters(BaseModel):
    input_value: str

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class SwitchTaskValueParamInputParameters(BaseModel):
    switch_case_value: str

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class SwitchTask(WorkflowTaskImpl):
    type: TaskType = TaskType.SWITCH
    default_case: list[WorkflowTaskImpl] | None = Field(default=[])  # type: ignore[assignment]
    decision_cases: dict[str, list[WorkflowTaskImpl]]
    evaluator_type: SwitchEvaluatorType = Field(default=SwitchEvaluatorType.JAVASCRIPT)
    expression: str
    input_parameters: SwitchTaskInputParameters | SwitchTaskValueParamInputParameters


class DecisionTaskInputParameters(BaseModel):
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)

    class Config:
        extra = Extra.allow


class DecisionTask(WorkflowTaskImpl):
    type: TaskType = TaskType.DECISION
    default_case: list[WorkflowTaskImpl] = []
    decision_cases: dict[str, list[WorkflowTaskImpl]]
    case_expression: str
    input_parameters: DecisionTaskInputParameters


class DecisionCaseValueTaskInputParameters(BaseModel):
    case_value_param: str


class DecisionCaseValueTask(WorkflowTaskImpl):
    type: TaskType = TaskType.DECISION
    default_case: list[WorkflowTaskImpl] = []
    decision_cases: dict[str, list[WorkflowTaskImpl]]
    case_value_param: str = 'case_value_param'
    input_parameters: DecisionCaseValueTaskInputParameters


class SubWorkflowInputParameters(BaseModel):
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)

    class Config:
        extra = Extra.allow


class SubWorkflowParam(BaseModel):
    name: str
    version: int
    task_to_domain: Optional[TaskToDomain] = Field(default=None)
    workflow_definition: Optional[WorkflowDef] = Field(default=None)


class SubWorkflowFromDefParam(BaseModel):
    name: type[Any]
    task_to_domain: Optional[TaskToDomain] = Field(default=None)
    workflow_definition: Optional[WorkflowDef] = Field(default=None)

    class Config:
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        validate_all = True


class SubWorkflowTask(WorkflowTaskImpl):
    type: TaskType = TaskType.SUB_WORKFLOW
    sub_workflow_param: SubWorkflowParam | SubWorkflowFromDefParam
    input_parameters: SubWorkflowInputParameters

    @root_validator(pre=True)
    def check_input_values(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        sub_wf_def = values['sub_workflow_param']
        worker_inputs = values['input_parameters'].dict()
        match sub_wf_def:
            case SubWorkflowFromDefParam():
                workflow_inputs = sub_wf_def.name.WorkflowInput().__fields__.items()
                for key, value in workflow_inputs:
                    if key not in worker_inputs:
                        if value.required is False:
                            pass
                        else:
                            raise ValueError(f'Missing input {key}')
                values['sub_workflow_param'] = SubWorkflowParam(
                    name=sub_wf_def.name.__name__,
                    version=sub_wf_def.name.__fields__['version'].default,
                )
        return values

    class Config:
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        validate_all = True


class SimpleTaskInputParameters(BaseModel):
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)

    class Config:
        extra = Extra.allow


class SimpleTask(WorkflowTaskImpl):
    name: object | str  # type: ignore[assignment]
    type: TaskType = TaskType.SIMPLE
    input_parameters: SimpleTaskInputParameters

    @root_validator(pre=True)
    def check_input_values(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        task_def = values['name']
        worker_inputs = values['input_parameters'].dict()

        match task_def:
            case type():
                if not issubclass(task_def, WorkerImpl):
                    raise ValueError('Bad input for name')
                values['name'] = task_def.WorkerDefinition.__fields__['name'].default
                task_input = task_def.WorkerInput.__fields__.items()
                for key, value in task_input:
                    if key not in worker_inputs:
                        if value.required is False:
                            pass
                        else:
                            raise ValueError(f'Missing input {key}')
        return values


class SetVariableTaskInputParameters(BaseModel):
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)

    class Config:
        extra = Extra.allow


class SetVariableTask(WorkflowTaskImpl):
    type: TaskType = TaskType.SET_VARIABLE
    input_parameters: SetVariableTaskInputParameters


class KafkaPublishTaskInputParameters(BaseModel):
    boot_strap_servers: str
    key: str
    key_serializer: str
    value: str
    request_timeout_ms: str
    max_block_ms: str
    headers: Optional[dict[str, Any]] = Field(default=None)
    topic: str

    class Config:
        alias_generator = snake_to_camel_case
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True


class KafkaPublishTask(WorkflowTaskImpl):
    type: TaskType = TaskType.KAFKA_PUBLISH
    input_parameters: KafkaPublishTaskInputParameters


class JsonJqTaskInputParameters(BaseModel):
    query_expression: str = Field(alias='queryExpression')

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = True
        extra = Extra.allow

    def __init__(self, query_expression: str, **data: Any) -> None:
        data['query_expression'] = query_expression
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


class JsonJqTask(WorkflowTaskImpl):
    type: TaskType = TaskType.JSON_JQ_TRANSFORM
    input_parameters: JsonJqTaskInputParameters


class JoinTask(WorkflowTaskImpl):
    type: TaskType = TaskType.JOIN
    join_on: list[str] = []


class ExclusiveJoinTask(WorkflowTaskImpl):
    type: TaskType = TaskType.EXCLUSIVE_JOIN
    join_on: list[str] = []


class EventTask(WorkflowTaskImpl):
    type: TaskType = TaskType.EVENT
    sink: str
    async_complete: bool
