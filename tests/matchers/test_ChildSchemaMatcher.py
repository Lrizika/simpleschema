
import typing
import re
from simpleschema.matchers import ChildSchemaMatcher
from simpleschema.exceptions import SchemaValidationFailure
from tests.matchers import matcher_test_framework


class TestChildSchemaMatcher(matcher_test_framework.TestMatcher):
	matcher = ChildSchemaMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = SchemaValidationFailure
	valid_pairs = [
		({str: int}, {'asdf': 1234}),
	]
	invalid_pairs = [
		({str: int}, {1234: 1234}),
	]
	inapplicable_constraints = ['asdf', typing.Any, typing.Iterable, r'.*', None, re.compile('asdf')]



