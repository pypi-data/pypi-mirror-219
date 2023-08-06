from unittest import TestCase
import json

from entail.results import TestResults, TestResult, PRF1, FnMatchResult

from entail import TestCase as ETestCase, Fn, Message, DesiredOutput


class TestTestResults(TestCase):

    def test_summarize_fn_results(self):
        tr = TestResults(results=[

        ])
        self.fail()

    def test_summarize_entailment_results(self):
        tr = TestResults(results=[

        ])
        self.fail()

    def test_summarize_reference_results(self):
        self.fail()

    def test_list_fn_results(self):
        self.fail()

    def test_list_entailment_results(self):
        self.fail()

    def test_list_reference_results(self):
        self.fail()

    def test_list_concerns(self):
        self.fail()


class TestTestResult(TestCase):
    def test_compare_function_name_match(self):
        tr = TestResult(
            case=ETestCase()
        )
        tr.compare_function(Fn(name='f1', args={}), Fn(name='f1', args={}))
        self.assertTrue(tr.function_match.name_match)

        tr = TestResult(
            case=ETestCase()
        )
        tr.compare_function(Fn(name='f1', args={3: 2}), Fn(name='f1', args={}))
        self.assertTrue(tr.function_match.name_match)

        tr = TestResult(
            case=ETestCase()
        )
        tr.compare_function(Fn(name='f1', args={}), Fn(name='f12', args={}))
        self.assertFalse(tr.function_match.name_match)

    def test_compare_function_args_both_empty(self):
        tr = TestResult(
            case=ETestCase()
        )
        tr.compare_function(Fn(name='f1', args={}), Fn(name='f1', args={}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 1.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.precision, 1.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 1.0,
        )

    def test_compare_function_args_expect_empty(self):
        tr = TestResult(
            case=ETestCase(),
        )
        tr.compare_function(Fn(name='f1', args={}), Fn(name='f1', args={3: 1}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.recall, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 0.0,
        )

    def test_compare_function_args_value_empty(self):
        tr = TestResult(
            case=ETestCase()
        )
        tr.compare_function(Fn(name='f1', args={'hello': 3}), Fn(name='f', args={}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.recall, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 0.0,
        )

    def test_compare_function_args_both_non_empty(self):
        tr = TestResult(
            case=ETestCase(),
        )
        tr.compare_function(Fn(name='f1', args={'hello': 3}), Fn(name='f1', args={'hello': 4}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.recall, 0.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 0.0,
        )

        tr = TestResult(
            case=ETestCase(),
        )
        tr.compare_function(Fn(name='f1', args={'hello': 3}), Fn(name='f1', args={'hello': 3, 'world': 3}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 0.5,
        )
        self.assertAlmostEqual(
            tr.function_match.args.recall, 1.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 2 / 3.0,
        )
        tr = TestResult(
            case=ETestCase(),
        )
        tr.compare_function(Fn(name='f1', args={'hello': 3, 2: 3}), Fn(name='f1', args={'hello': 3}))
        self.assertAlmostEqual(
            tr.function_match.args.precision, 1.0,
        )
        self.assertAlmostEqual(
            tr.function_match.args.recall, 0.5,
        )
        self.assertAlmostEqual(
            tr.function_match.args.f1, 2 / 3.0,
        )

    def test_get_concern(self):
        tr = TestResult(
            case=ETestCase(
                output=DesiredOutput(
                    exact='world'
                ),
            ),
            reply=Message.from_assistant('hello'),
            exact_match=False,
        )

        c = tr.get_concern()
        self.assertEqual(c.reasons, [f'Response does not match: \n '
                                     f'Expected: world \n '
                                     f'Received: hello \n'])

        tr = TestResult(
            case=ETestCase(
                reply=Message.from_assistant(Fn(name='f1', args={})),
                output=DesiredOutput(
                    should_call_function=Fn(name='f1', args={'hello': '2'})
                ),
            ),
            reply=Message.from_assistant('hello'),
            function_match=FnMatchResult(name_match=True, args=PRF1(precision=0.0, recall=0.0, f1=0.0)),
        )

        c = tr.get_concern()
        self.assertEqual(c.reasons, [
            (f'Function Args does not match: \n '
             f'Expected: {json.dumps({"hello": "2"}, sort_keys=True)} \n '
             f'Received: {json.dumps({}, sort_keys=True)} \n')
        ])
