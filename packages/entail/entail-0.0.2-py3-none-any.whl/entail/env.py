from dataclasses import dataclass, field

from entail import ChatHandler, create_default_entailment, RunConfig, TestCase, utils, \
    RuleMatch, Quantifier, Hypothesis
from entail.results import TestResult, TestResults
from entail.entailment import EntailmentModel


@dataclass
class NewTestEnv:
    handler: ChatHandler = None
    entailment: EntailmentModel = None
    config: RunConfig = None
    tests: list[TestCase] = field(default_factory=list)

    def create(self):

        if self.handler is None:
            raise ValueError('There is no ChatHandler to be tested, see .will_be_testing(your_handler)')

        if self.tests is None:
            raise ValueError('There is no testcases, using with_tests or with_test to add test cases')

        if self.config is None:
            self.config = RunConfig()

        if self.entailment is None:
            self.entailment = create_default_entailment()

        return TestEnv(
            self.handler,
            entailment=self.entailment,
            config=self.config,
            tests=self.tests,
        )

    def will_be_testing(self, handler: ChatHandler):
        self.handler = handler
        return self

    def with_tests(self, tests):
        for t in tests:
            self.tests.append(t)
        return self

    def with_test(self, t):
        self.tests.append(t)
        return self

    def using_config(self, config):
        self.config = config
        return self


@dataclass
class TestEnv:
    handler: ChatHandler
    entailment: EntailmentModel = field(default_factory=create_default_entailment)
    config: RunConfig = field(default_factory=RunConfig)
    tests: list[TestCase] = field(default_factory=list)

    def run_tests(self, tags=None, name=None):
        todo = []
        if tags is not None:
            for testcase in self.tests:
                match_tag = False
                for t in testcase.tags:
                    for mt in tags:
                        if t == mt:
                            match_tag = True
                            break
                todo.append(testcase)
        elif name is not None:
            for testcase in self.tests:
                if testcase.name == name:
                    todo.append(testcase)
        else:
            todo = [t for t in self.tests]

        results = []
        for t in todo:
            ret = self.run_test(t)
            results.append(ret)
        return TestResults(results=results)

    def run_test(self, testcase: TestCase) -> TestResult:
        result = TestResult(
            case=testcase,
        )
        reply = self.handler.response(testcase.history, external_information=testcase.external_info)
        if reply.fn:
            if self.config.function:
                result.compare_function(testcase.output.should_call_function, reply.fn)
        elif reply.content:
            if testcase.output.exact:
                result.exact_match = testcase.output.exact == reply.content
            else:
                if testcase.output.example:
                    if self.config.bleu:
                        result.bleu = utils.bleu(testcase.output.example, reply.content)
                    if self.config.rouge:
                        result.rouge = utils.rouge(testcase.output.example, reply.content)
                    if self.config.meteor:
                        result.meteor = utils.meteor(testcase.output.example, reply.content)

                if testcase.output.should_be:
                    if self.config.entail:
                        for hypothesis in testcase.output.should_be:
                            score = test_hypothesis(hypothesis, self.entailment, reply.content)
                            result.entails.append(RuleMatch(hypothesis=hypothesis, score=score))
        else:
            result.is_empty = True

        return result


def test_hypothesis(hypothesis: Hypothesis, entailment: EntailmentModel, content: str):
    if hypothesis.quantifier == Quantifier.any_of:
        return max([test_hypothesis(x, entailment, content) for x in hypothesis.children])
    elif hypothesis.quantifier == Quantifier.all_of:
        return min([test_hypothesis(x, entailment, content) for x in hypothesis.children])
    elif hypothesis.quantifier == Quantifier.none_of:
        return max([1 - test_hypothesis(x, entailment, content) for x in hypothesis.children])
    elif hypothesis.quantifier is None:
        score = entailment.entail(content, hypothesis.value)
        return score
