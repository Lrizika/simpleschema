
import unittest
import typing
import re
import logging
from simpleschema.matchers import RegExMatcher
from simpleschema.exceptions import RegExMismatch

logger = logging.getLogger(__name__)


class TestRegExMatcher(unittest.TestCase):
	valid_pairs = {
		re.compile(r'.*'): 'asdf',
	}
	invalid_pairs = {
		re.compile(r'asdf'): 'fdsa',
	}
	inapplicable_constraints = ['asdf']

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

