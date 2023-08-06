import random
import time
from typing import Optional

from frinx.common.conductor_enums import TaskResultStatus
from frinx.common.type_aliases import DictAny
from frinx.common.type_aliases import ListAny
from frinx.common.worker.service import ServiceWorkersImpl
from frinx.common.worker.task_def import TaskDefinition
from frinx.common.worker.task_def import TaskInput
from frinx.common.worker.task_def import TaskOutput
from frinx.common.worker.task_result import TaskResult
from frinx.common.worker.worker import WorkerImpl


class TestWorker(ServiceWorkersImpl):
    class Echo(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name: str = 'TEST_echo'
            description: str = 'testing purposes: returns input unchanged'
            labels: ListAny = ['TEST']
            timeout_seconds: int = 60
            response_timeout_seconds: int = 60

        class WorkerInput(TaskInput):
            input: str

        class WorkerOutput(TaskOutput):
            output: str

        def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
            return TaskResult(
                status=TaskResultStatus.COMPLETED,
                logs=['Echo worker invoked successfully'],
                output=self.WorkerOutput(output=worker_input.input)
            )

    class Sleep(WorkerImpl):
        DEFAULT_SLEEP = 10
        MAX_SLEEP = 600

        class WorkerDefinition(TaskDefinition):
            name: str = 'TEST_sleep'
            description: str = 'testing purposes: sleep'
            labels: ListAny = ['TEST']
            timeout_seconds: int = 600
            response_timeout_seconds: int = 600

        class WorkerInput(TaskInput):
            time: int | None = 10

        class WorkerOutput(TaskOutput):
            time: int

        def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
            sleep = worker_input.time if worker_input.time else self.DEFAULT_SLEEP
            if sleep < 0 or sleep > self.MAX_SLEEP:
                return TaskResult(
                    status=TaskResultStatus.FAILED,
                    logs=['Invalid sleep time, must be > 0 and < 600'],
                )

            time.sleep(sleep)
            return TaskResult(
                status=TaskResultStatus.COMPLETED,
                logs=['Sleep worker invoked. Sleeping'],
                output=self.WorkerOutput(time=sleep)
            )

    class DynamicForkGenerator(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name: str = 'TEST_dynamic_fork_generate'
            description: str = 'testing purposes: generate dynamic fork tasks'
            labels: ListAny = ['TEST']
            timeout_seconds: int = 60
            response_timeout_seconds: int = 60

        class WorkerInput(TaskInput):
            wf_count: int = 10
            wf_name: str = 'Test_workflow'
            wf_inputs: Optional[DictAny] = {}

        class WorkerOutput(TaskOutput):
            dynamic_tasks_i: DictAny
            dynamic_tasks: ListAny

        def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
            wf_count = worker_input.wf_count
            wf_name = worker_input.wf_name
            wf_inputs = worker_input.wf_inputs
            dynamic_tasks = []
            dynamic_tasks_i = {}

            for task_ref in range(0, wf_count):
                dynamic_tasks.append(
                    {
                        'name': 'sub_task',
                        'taskReferenceName': str(task_ref),
                        'type': 'SUB_WORKFLOW',
                        'subWorkflowParam': {'name': wf_name, 'version': 1},
                    }
                )
                dynamic_tasks_i[str(task_ref)] = wf_inputs

            return TaskResult(
                status=TaskResultStatus.COMPLETED,
                logs=['Dynamic fork generator worker invoked successfully'],
                output=self.WorkerOutput(
                    dynamic_tasks_i=dynamic_tasks_i,
                    dynamic_tasks=dynamic_tasks
                )
            )

    class LoremIpsum(WorkerImpl):
        class WorkerDefinition(TaskDefinition):
            name: str = 'TEST_lorem_ipsum'
            description: str = 'testing purposes: text generator'
            labels: ListAny = ['TEST']
            timeout_seconds: int = 60
            response_timeout_seconds: int = 60

        class WorkerInput(TaskInput):
            num_paragraphs: int = 3
            num_sentences: int = 3
            num_words: int = 3

        class WorkerOutput(TaskOutput):
            text: str
            bytes: int

        def execute(self, worker_input: WorkerInput) -> TaskResult[WorkerOutput]:
            text = generate_text(
                num_paragraphs=worker_input.num_paragraphs,
                num_sentences=worker_input.num_sentences,
                num_words=worker_input.num_words,
            )

            return TaskResult(
                status=TaskResultStatus.COMPLETED,
                logs=['Lorem ipsum worker invoked successfully'],
                output=self.WorkerOutput(
                    text=text,
                    bytes=len(text.encode('utf-8'))
                )
            )


WORDS = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit']


def generate_sentence(num_words: int) -> str:
    sentence = []
    for i in range(num_words):
        sentence.append(random.choice(WORDS))
    return ' '.join(sentence).capitalize() + '.'


def generate_paragraph(num_sentences: int, num_words: int) -> str:
    paragraph = []
    for i in range(num_sentences):
        paragraph.append(generate_sentence(num_words))
    return ' '.join(paragraph)


def generate_text(num_paragraphs: int, num_sentences: int, num_words: int) -> str:
    text = []
    for i in range(num_paragraphs):
        text.append(generate_paragraph(num_sentences, num_words))
    return '\n\n'.join(text)
