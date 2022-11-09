
import unittest
import typing
import re
import logging
from simpleschema.matchers import ConstraintMatcher

logger = logging.getLogger(__name__)


class TestConstraintMatcher(unittest.TestCase):
	constraints = [None, typing.Any, '', 'asdf', re.compile(r'.*'), callable]
	items = [None, typing.Any, '', 'asdf', re.compile(r'.*'), callable]

	def test_isApplicable_True(self):
		for constraint in self.constraints:
			with self.assertRaises(
					NotImplementedError,
					msg=f'Failed with constraint {constraint}'
			) as context:
				ConstraintMatcher.isApplicable(constraint)
				ConstraintMatcher().isApplicable(constraint)
			logger.debug(context.exception)

	def test_isApplicable_False(self):
		pass

	def test_validate_success(self):
		for constraint in self.constraints:
			for item in self.items:
				with self.assertRaises(
						NotImplementedError,
						msg=f'Failed with constraint {constraint}, item {item}'
				) as context:
					ConstraintMatcher.validate(item, constraint)
					ConstraintMatcher().validate(item, constraint)
				logger.debug(context.exception)

	def test_validate_failure(self):
		pass

