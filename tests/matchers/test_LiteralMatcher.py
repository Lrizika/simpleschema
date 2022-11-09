
import typing
import re
from simpleschema.matchers import LiteralMatcher
from simpleschema.exceptions import LiteralMismatch
import simpleschema
from tests.matchers import matcher_test_framework


class TestLiteralMatcher(matcher_test_framework.TestMatcher):
	matcher = LiteralMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = LiteralMismatch
	valid_pairs = [
		(typing.Literal[1234], 1234),
		(typing.Literal['asdf'], 'asdf'),
		(typing.Literal[None], None),
		(typing.Literal[True], True),
		(simpleschema.Literal(callable), callable),
		(simpleschema.Literal(re), re),
	]
	invalid_pairs = [
		(typing.Literal[1234], 1),
		(simpleschema.Literal(callable), lambda _: True),
	]
	inapplicable_constraints = ['asdf', typing.Any, typing.Iterable, r'.*', None, re.compile('asdf')]



