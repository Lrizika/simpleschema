
import unittest
import typing
import re
import logging
from simpleschema.matchers import RegExMatcher
from simpleschema.exceptions import RegExMismatch

logger = logging.getLogger(__name__)


class TestRegExMatcher(unittest.TestCase):
	# Many of these test cases were stolen from the python re tests
	valid_pairs = {
		re.compile(r'.*'): 'asdf',
		re.compile(r''): '',
		re.compile(r'abc'): 'abc',
		re.compile(r'abc'): 'xabcy',
		re.compile(r'abc'): 'ababc',
		re.compile(r'ab*c'): 'abc',
		re.compile(r'ab*bc'): 'abc',
		re.compile(r'ab*bc'): 'abbc',
		re.compile(r'ab*bc'): 'abbbbc',
		re.compile(r'ab+bc'): 'abbc',
		re.compile(r'ab+bc'): 'abbbbc',
		re.compile(r'ab?bc'): 'abbc',
		re.compile(r'ab?bc'): 'abc',
		re.compile(r'ab?c'): 'abc',
		re.compile(r'^abc$'): 'abc',
	}
	invalid_pairs = {
		re.compile(r'asdf'): 'fdsa',
		re.compile(r'a..f'): 'fafa',
		re.compile(r'abc'): 'xbc',
		re.compile(r'abc'): 'axc',
		re.compile(r'ab+bc'): 'abc',
		re.compile(r'ab+bc'): 'abq',
		re.compile(r'abc'): 'abx',
		re.compile(r'ab?bc'): 'abbbbc',
	}
	inapplicable_constraints = ['asdf', typing.Any, typing.Iterable, r'.*', None]

	def test_isApplicable_True(self):
		for constraint in list(self.valid_pairs.keys()) + list(self.invalid_pairs.keys()):
			self.assertTrue(
				RegExMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertTrue(
				RegExMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_isApplicable_False(self):
		for constraint in self.inapplicable_constraints:
			self.assertFalse(
				RegExMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertFalse(
				RegExMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_validate_success(self):
		for constraint, item in self.valid_pairs.items():
			self.assertTrue(
				RegExMatcher.validate(item, constraint),
				msg=f'Failed with constraint {constraint}, item {item}'
			)
			self.assertTrue(
				RegExMatcher().validate(item, constraint),
				msg=f'Failed with constraint {constraint}, item {item}'
			)

	def test_validate_failure(self):
		for constraint, item in self.invalid_pairs.items():
			with self.assertRaises(
					RegExMismatch,
					msg=f'Failed with constraint {constraint}, item {item}'
			) as context:
				RegExMatcher.validate(item, constraint)
				RegExMatcher().validate(item, constraint)
			logger.debug(context.exception)

