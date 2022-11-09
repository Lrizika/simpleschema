
import typing
import re
from simpleschema.matchers import AnyMatcher
from tests.matchers import matcher_test_framework


class TestAnyMatcher(matcher_test_framework.TestMatcher):
	matcher = AnyMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = None
	valid_pairs = [
		(typing.Any, 1234),
		(typing.Any, 'asdf'),
		(typing.Any, None),
		(typing.Any, True),
		(typing.Any, callable),
		(typing.Any, re),
		(typing.Any, re.compile(r'.*')),
	]
	invalid_pairs = []
	inapplicable_constraints = [None, '', 'asdf', re.compile(r'.*'), callable]
