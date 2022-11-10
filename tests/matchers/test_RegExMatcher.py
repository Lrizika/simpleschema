
import typing
import re
import simpleschema
from simpleschema.matchers import RegExMatcher
from simpleschema.exceptions import RegExMismatch
from tests.matchers import matcher_test_framework


class TestRegExMatcher(matcher_test_framework.TestMatcher):
	matcher = RegExMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = RegExMismatch
	# Many of these test cases were stolen from the python re tests
	valid_pairs = [
		(re.compile(r'.*'), 'asdf'),
		(re.compile(r''), ''),
		(re.compile(r'abc'), 'abc'),
		(re.compile(r'abc'), 'xabcy'),
		(re.compile(r'abc'), 'ababc'),
		(re.compile(r'ab*c'), 'abc'),
		(re.compile(r'ab*bc'), 'abc'),
		(re.compile(r'ab*bc'), 'abbc'),
		(re.compile(r'ab*bc'), 'abbbbc'),
		(re.compile(r'ab+bc'), 'abbc'),
		(re.compile(r'ab+bc'), 'abbbbc'),
		(re.compile(r'ab?bc'), 'abbc'),
		(re.compile(r'ab?bc'), 'abc'),
		(re.compile(r'ab?c'), 'abc'),
		(re.compile(r'^abc$'), 'abc'),
		(simpleschema.constraints.RegEx(r'ab?bc'), 'abbc'),
		(simpleschema.constraints.RegEx(r'ab?bc'), 'abc'),
		(simpleschema.constraints.RegEx(r'ab?c'), 'abc'),
		(simpleschema.constraints.RegEx(r'^abc$'), 'abc'),
	]
	invalid_pairs = [
		(re.compile(r'asdf'), 'fdsa'),
		(re.compile(r'a..f'), 'fafa'),
		(re.compile(r'abc'), 'xbc'),
		(re.compile(r'abc'), 'axc'),
		(re.compile(r'ab+bc'), 'abc'),
		(re.compile(r'ab+bc'), 'abq'),
		(re.compile(r'abc'), 'abx'),
		(re.compile(r'ab?bc'), 'abbbbc'),
		(simpleschema.constraints.RegEx(r'ab?bc'), 'abbbbc'),
	]
	inapplicable_constraints = ['asdf', typing.Any, typing.Iterable, r'.*', None]
