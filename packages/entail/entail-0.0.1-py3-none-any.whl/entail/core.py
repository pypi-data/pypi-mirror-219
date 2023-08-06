import abc
import os
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ChatHandler(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def response(self, chat_history: list['Message'], external_information: Optional[dict] = None) -> 'Message':
        raise NotImplementedError()


class Should:
    @staticmethod
    def be_any_of(*args):
        for cond in args:
            pass


class Quantifier(str, Enum):
    any_of = 'any_of'
    all_of = 'all_of'
    none_of = 'none_of'


class Hypothesis(BaseModel):
    quantifier: Optional[Quantifier] = None
    children: Optional[list['Hypothesis']] = None
    value: Optional[str] = None

    @staticmethod
    def any_of(children: list['Hypothesis']):
        return Hypothesis(quantifier=Quantifier.any_of, children=children)

    @staticmethod
    def all_of(children: list['Hypothesis']):
        return Hypothesis(quantifier=Quantifier.all_of, children=children)

    @staticmethod
    def none_of(children: list['Hypothesis']):
        return Hypothesis(quantifier=Quantifier.none_of, children=children)

    @staticmethod
    def of(value: str):
        return Hypothesis(quantifier=None, value=value)


class Role(str, Enum):
    system = 'system'
    user = 'user'
    assistant = 'assistant'
    function = 'function'


class Fn(BaseModel):
    name: str
    args: dict


class Message(BaseModel):
    role: Role
    content: Optional[str] = None
    fn: Optional[Fn] = None

    @staticmethod
    def from_user(value):
        return Message._create(Role.user, value)

    @staticmethod
    def from_assistant(value):
        return Message._create(Role.assistant, value)

    @staticmethod
    def _create(role, value):
        if isinstance(value, str):
            return Message(role=role, content=value)
        elif isinstance(value, Fn):
            return Message(role=role, fn=value)
        else:
            raise ValueError(f'Message value must be str or Fn')


class DesiredOutput(BaseModel):
    """
    A class describing the desired output of a chat message.

    When describing a desired text output, you should supply at least one of the example, exact, and should_be field
    When describing a desired function call output, you should supply should_call_function

    example: A reference response.
    should_be:
    should_call_function: what function should the response call
    """

    example: Optional[str] = None
    exact: Optional[str] = None
    should_be: Optional[list[Hypothesis]] = None
    should_call_function: Optional[Fn] = None


class TestCase(BaseModel):
    """
    A test case for chat model
    name: A optional name for this testcase, i.e. you can run a testcase by name
    description: A description of what is this test case testing.
    tags:  A list of tags for this testcase, i.e. you can run a list of testcases contains a certain tag
    external_info: a dict of external information should be supplied to the chat handler.
                   for example, in real application, this could be user info retrieved from database.
    history: chat history
    output: describe the desired output
    """
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    external_info: Optional[dict] = None
    history: list[Message] = Field(default_factory=list)
    output: DesiredOutput = Field(default_factory=DesiredOutput)
    path: str = ''


class RuleMatch(BaseModel):
    hypothesis: Hypothesis
    score: float


def create_default_entailment():
    from entail.entailment.hf import HFEntailment
    return HFEntailment()


def create_testing_env(test_folder, testing=None, ):
    pass


def load_tests_from_str(content):
    local_ctx = {}
    exec(content, globals(), local_ctx)
    for k, v in local_ctx.items():
        if isinstance(v, TestCase):
            yield v


def load_testcases(folder_path):
    extensions = ['.entail.py']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path.endswith(ext) for ext in extensions):
                with open(file_path) as fd:
                    for cases in load_tests_from_str(fd.read()):
                        yield cases
