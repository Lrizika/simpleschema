
import unittest
import typing
import re
import logging
from simpleschema.matchers import LiteralMatcher
from simpleschema.exceptions import LiteralMismatch
import simpleschema

logger = logging.getLogger(__name__)


class TestLiteralMatcher(unittest.TestCase):
	# Many of these test cases were stolen from the python re tests
	valid_pairs = {
		typing.Literal[1234]: 1234,
		typing.Literal['asdf']: 'asdf',
		typing.Literal[None]: None,
		typing.Literal[True]: True,
		simpleschema.Literal(callable): callable,
		simpleschema.Literal(re): re,
	}
	invalid_pairs = {
		typing.Literal[1234]: 1,
		simpleschema.Literal(callable): lambda _: True,
	}
	inapplicable_constraints = ['asdf', typing.Any, typing.Iterable, r'.*', None, re.compile('asdf')]

	def test_isApplicable_True(self):
		for constraint in list(self.valid_pairs.keys()) + list(self.invalid_pairs.keys()):
			self.assertTrue(
				LiteralMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertTrue(
				LiteralMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_isApplicable_False(self):
		for constraint in self.inapplicable_constraints:
			self.assertFalse(
				LiteralMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertFalse(
				LiteralMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_validate_success(self):
		for constraint, item in self.valid_pairs.items():
			self.assertTrue(
				LiteralMatcher.validate(item, constraint),
				msg=f'Failed with constraint {constraint}, item {item}'
			)
			self.assertTrue(
				LiteralMatcher().validate(item, constraint),
				msg=f'Failed with constraint {constraint}, item {item}'
			)

	def test_validate_failure(self):
		for constraint, item in self.invalid_pairs.items():
			with self.assertRaises(
					LiteralMismatch,
					msg=f'Failed with constraint {constraint}, item {item}'
			) as context:
				LiteralMatcher.validate(item, constraint)
				LiteralMatcher().validate(item, constraint)
			logger.debug(context.exception)

