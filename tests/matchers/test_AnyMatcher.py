
import unittest
import typing
import re
import logging
from simpleschema.matchers import AnyMatcher

logger = logging.getLogger(__name__)


class TestAnyMatcher(unittest.TestCase):
	applicable_constraints = [typing.Any]
	inapplicable_constraints = [None, '', 'asdf', re.compile(r'.*'), callable]
	items = [None, typing.Any, '', 'asdf', re.compile(r'.*'), callable]

	def test_isApplicable_True(self):
		for constraint in self.applicable_constraints:
			self.assertTrue(
				AnyMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertTrue(
				AnyMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_isApplicable_False(self):
		for constraint in self.inapplicable_constraints:
			self.assertFalse(
				AnyMatcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertFalse(
				AnyMatcher().isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_validate_success(self):
		for constraint in self.applicable_constraints:
			for item in self.items:
				self.assertTrue(
					AnyMatcher.validate(item, constraint),
					msg=f'Failed with constraint {constraint}, item {item}'
				)
				self.assertTrue(
					AnyMatcher().validate(item, constraint),
					msg=f'Failed with constraint {constraint}, item {item}'
				)

	def test_validate_failure(self):
		pass

