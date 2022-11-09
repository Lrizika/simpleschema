
import typing
import re
from simpleschema.matchers import TypeMatcher
from simpleschema.exceptions import TypeMismatch
import simpleschema
from tests.matchers import matcher_test_framework


class TestTypeMatcher(matcher_test_framework.TestMatcher):
	matcher = TypeMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = TypeMismatch
	valid_pairs = [
		(int, 1234),
		(str, 'asdf'),
		(typing.Callable, lambda _: True),
		(typing.Iterable, [1, 2, 3]),
		(simpleschema.Literal, simpleschema.Literal(1234)),
	]
	invalid_pairs = [
		(int, 'asdf'),
		(str, 1234),
		(typing.Callable, 1234),
	]
	inapplicable_constraints = ['asdf', r'.*', None, re.compile('asdf'), simpleschema.Literal(int)]



