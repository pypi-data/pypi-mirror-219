from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field

from entail.core import RuleMatch, Fn, TestCase


class PRF1(BaseModel):
    precision: float
    recall: float
    f1: float


class FnMatchResult(BaseModel):
    name_match: bool
    args: PRF1


class TestResult(BaseModel):
    case: TestCase

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

    def compare_function(self, expected: Fn, value: Fn):
        name_match = expected.name == value.name
        rr_count = len(set(expected.args.items()).intersection(set(value.args.items())))
        p = rr_count * 1.0 / len(value.args) if len(value.args) > 0 else 0.0
        r = rr_count * 1.0 / len(expected.args) if len(expected.args) > 0 else 0.0
        f1 = 2 * p * r / (p + r)
        args_prf1 = PRF1(precision=p, recall=r, f1=f1)
        self.function_match = FnMatchResult(name_match=name_match, args=args_prf1)


@dataclass
class TestResults:
    results: list['TestResult']

    def summarize(self):
        pass

    def summarize_fn_results(self):
        pass

    def summarize_entailment_results(self):
        pass

    def summarize_reference_results(self):
        exact_match_cases = 0
        exact_match_failed = 0

        exact_match_cases = 0
        exact_match_failed = 0

        rs = self.list_reference_results()
        for r in rs:
            if r.exact_match is not None:
                exact_match_cases += 1
            if r.exact_match is True:
                exact_match_failed += 1

    def list_fn_results(self):
        rs = []
        for r in self.results:
            if r.function_match is not None:
                rs.append(r)

    def list_entailment_results(self):
        rs = []
        for r in self.results:
            if r.entails is not None and len(r.entails) > 0:
                rs.append(r)

    def list_reference_results(self):
        rs = []
        for r in self.results:
            if r.case.output.exact is not None or r.case.output.example is not None:
                rs.append(r)
        return rs
