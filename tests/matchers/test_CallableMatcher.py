
import re
from simpleschema.matchers import CallableMatcher
from simpleschema.exceptions import CallableMismatch
import simpleschema
from tests.matchers import matcher_test_framework


class TestCallableMatcher(matcher_test_framework.TestMatcher):
	matcher = CallableMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = CallableMismatch
	valid_pairs = [
		(lambda v: v > 10, 1234),
		(lambda v: v < 10, 1),
		(str, 'asdf'),
		(callable, lambda _: True),
		(callable, callable),
		(bool, 1),
		(simpleschema.constraints.Callable(lambda v: v > 10), 1234),
	]
	invalid_pairs = [
		(lambda v: v > 10, 1),
		(lambda v: v < 10, 1234),
		(callable, 1234),
		(bool, 0),
		(simpleschema.constraints.Callable(lambda v: v > 10), 1),
	]
	inapplicable_constraints = ['asdf', r'.*', None, re.compile('asdf'), simpleschema.constraints.Literal(int)]



