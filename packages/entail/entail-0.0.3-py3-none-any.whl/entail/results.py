import json
import sys
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field

from entail import RunConfig
from entail.core import RuleMatch, Fn, TestCase, Message


class PRF1(BaseModel):
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0

    def print(self, out=None, padding=0):
        if out is None:
            out = sys.stdout
        pads = ' ' * padding
        print(f'{pads}Precision  : {self.precision:.2f}', file=out)
        print(f'{pads}Recall     : {self.recall:.2f}', file=out)
        print(f'{pads}F1         : {self.f1:.2f}', file=out)

    def __eq__(self, other):
        return self.precision == other.precision and self.recall == other.recall and self.f1 == other.f1


class FnMatchResult(BaseModel):
    name_match: bool
    args: PRF1


class TestResult(BaseModel):
    case: TestCase
    reply: Optional[Message]

    # Referential testing
    exact_match: Optional[bool] = None
    bleu: Optional[float] = None
    rouge: Optional[PRF1] = None
    meteor: Optional[float] = None
    # Entail testing
    entails: list[RuleMatch] = Field(default_factory=list)
    # Function Call Testing
    function_match: Optional[FnMatchResult] = None

    is_empty: bool = False

    def compare_function(self, expected: Fn, value: Optional[Fn]):
        name_match = expected.name == value.name if value is not None else False

        if value is None:
            args_prf1 = PRF1(precision=0.0, recall=0.0, f1=0.0)
        else:
            if len(expected.args) == 0 and len(value.args) == 0:
                args_prf1 = PRF1(precision=1.0, recall=1.0, f1=1.0)
            else:
                rr_count = len(set(expected.args.items()).intersection(set(value.args.items())))
                p = rr_count * 1.0 / len(value.args) if len(value.args) > 0 else 0.0
                r = rr_count * 1.0 / len(expected.args) if len(expected.args) > 0 else 0.0
                f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
                args_prf1 = PRF1(precision=p, recall=r, f1=f1)
        self.function_match = FnMatchResult(name_match=name_match, args=args_prf1)

    def get_concern(self) -> 'TestingConcern':
        concern = TestingConcern()
        if self.exact_match is False:
            concern.append(f'Response does not match: \n '
                           f'Expected: {self.case.output.exact} \n '
                           f'Received: {self.reply.content} \n')

        if self.function_match is not None:
            if self.function_match.name_match is False:
                concern.append(f'Function Name does not match: \n '
                               f'Expected: {self.case.output.should_call_function.name} \n '
                               f'Received: {self.reply.fn.name} \n')
            if self.function_match.args.f1 != 1.0:
                concern.append(f'Function Args does not match: \n '
                               f'Expected: {json.dumps(self.case.output.should_call_function.args, sort_keys=True)} \n '
                               f'Received: {json.dumps(self.reply.fn.args, sort_keys=True)} \n')
        if self.entails:
            for rm in self.entails:
                if rm.score <= 0.5:
                    concern.append(f'Entailment Rule failed: \n '
                                   f'Rule: {rm.hypothesis} \n '
                                   f'Response: {self.reply.fn.args} \n')

        return concern


class TestingConcern(BaseModel):
    reasons: list[str] = Field(default_factory=list)

    def append(self, reason):
        self.reasons.append(reason)

    def is_valid(self):
        return len(self.reasons) > 0


class FnTestSummary(BaseModel):
    average: PRF1 = Field(default_factory=PRF1)
    name_matched: int = 0
    total: int = 0

    def print(self, out=None):
        if out is None:
            out = sys.stdout
        print(f"[Fn Tests]", file=out)
        print(f"Total                 :   {self.total}", file=out)
        print(f"Total Name Matches    :   {self.name_matched}", file=out)
        print(f"Total Name Mismatches :   {self.total - self.name_matched}", file=out)

        print(f"[Average Args Matches]", file=out)
        self.average.print(out=out, padding=4)


class EntailmentTestSummary(BaseModel):
    test_performed: int = 0
    average_score: float = 0.0

    def print(self, out=None):
        if out is None:
            out = sys.stdout
        print(f"Total Entailment Tests  : {self.test_performed}", file=out)
        print(f"Average Score           : {self.average_score:.2f}", file=out)


class ReferenceTestSummary(BaseModel):
    exact_math_positive: int = 0
    exact_math_negative: int = 0

    non_exact_test_count: int = 0
    bleu_average: Optional[float] = None
    rouge_average: Optional[PRF1] = None
    meteor_average: Optional[float] = None

    @property
    def exact_match_total(self):
        return self.exact_math_positive + self.exact_math_negative

    def print(self, out=None):
        if out is None:
            out = sys.stdout
        print(f"[Exact Matches Tests]", file=out)
        print(f"Positive           : {self.exact_math_positive}", file=out)
        print(f"Negative           : {self.exact_math_negative}", file=out)
        print(f"Total              : {self.exact_match_total}", file=out)
        print("", file=out)

        print(f"[Non Exact Matching Tests]", file=out)
        print(f"Total                   : {self.non_exact_test_count}", file=out)
        if self.bleu_average is not None:
            print(f"Average BLEU            : {self.bleu_average:.2f}", file=out)
        if self.meteor_average is not None:
            print(f"Average METEOR          : {self.meteor_average:.2f}", file=out)
        if self.rouge_average is not None:
            print(f"Average ROUGE", file=out)
            self.rouge_average.print(out, padding=4)


def mean_prf1(prf1s: list[PRF1]) -> PRF1:
    l = len(prf1s)
    p, r, f1 = 0.0, 0.0, 0.0
    if l == 0:
        return PRF1()
    for prf1 in prf1s:
        p += prf1.precision
        r += prf1.recall
        f1 += prf1.f1
    return PRF1(
        precision=p / l, recall=r / l, f1=f1 / l
    )


@dataclass
class TestResults:
    results: list['TestResult']
    config: RunConfig

    def summarize_fn_results(self) -> FnTestSummary:
        ret = FnTestSummary()
        ts = self.list_fn_results()
        ret.total = len(ts)
        ret.name_matched = len([t for t in ts if t.function_match.name_match])
        ret.average = mean_prf1([t.function_match.args for t in ts])
        return ret

    def summarize_entailment_results(self) -> EntailmentTestSummary:
        ret = EntailmentTestSummary()
        ts = self.list_entailment_results()
        scores = []
        for t in ts:
            ret.test_performed += 1
            for rm in t.entails:
                scores.append(rm.score)

        ret.average_score = len(scores) * 1.0 / len(scores)

        return ret

    def summarize_reference_results(self) -> ReferenceTestSummary:
        ret = ReferenceTestSummary()
        rs = self.list_reference_results()
        bleu = []
        rouge = []
        meteor = []
        for r in rs:
            if r.exact_match is not None:
                if r.exact_match is True:
                    ret.exact_math_positive += 1
                else:
                    ret.exact_math_negative += 1
            non_exact = False
            if self.config.bleu and r.bleu is not None:
                non_exact = True
                bleu.append(r.bleu)

            if self.config.meteor and r.meteor is not None:
                non_exact = True
                meteor.append(r.meteor)

            if self.config.rouge and r.rouge is not None:
                non_exact = True
                rouge.append(r.rouge)

            if non_exact:
                ret.non_exact_test_count += 1
        if self.config.meteor:
            ret.meteor_average = sum(meteor) * 1.0 / len(meteor) if len(meteor) > 0 else 0.0
        else:
            ret.meteor_average = None

        if self.config.bleu:
            ret.bleu_average = sum(bleu) * 1.0 / len(bleu) if len(bleu) > 0 else 0.0
        else:
            ret.bleu_average = None

        if self.config.rouge:
            ret.rouge_average = mean_prf1(rouge)
        else:
            ret.rouge_average = None

        return ret

    def list_fn_results(self):
        rs = []
        for r in self.results:
            if r.function_match is not None:
                rs.append(r)

        return rs

    def list_entailment_results(self):
        rs = []
        for r in self.results:
            if r.entails is not None and len(r.entails) > 0:
                rs.append(r)

        return rs

    def list_reference_results(self):
        rs = []
        for r in self.results:
            if r.case.output.exact is not None or r.case.output.example is not None:
                rs.append(r)
        return rs

    def print(self, out=None):
        if self.config.entail:
            self.summarize_entailment_results().print(out)
        r = self.summarize_reference_results()
        if r.exact_match_total > 0 or self.config.bleu or self.config.rouge or self.config.meteor:
            r.print(out)
        if self.config.function:
            self.summarize_fn_results().print(out)

    def list_concerns(self):
        for t in self.results:
            concern = t.get_concern()
            if concern.is_valid():
                yield t, concern

    def print_test_summary(self, out=None):
        if out is None:
            out = sys.stdout
        cs = list(self.list_concerns())
        if len(cs) == 0:
            print('OK', file=out)
        else:
            print('The following tests have concerns:', file=out)
            for idx, (t, c) in enumerate(cs):
                print(f"[{idx:03d}] Case name: {t.case.name}")
                print(f"Reply: {t.reply}")
                for reason in c.reasons:
                    print(reason, file=out)
                print('-------\n')
