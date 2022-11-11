
import unittest
import logging
from simpleschema.validate import default_validator

logger = logging.getLogger(__name__)


class TestMatcher(unittest.TestCase):
	matcher = None
	matcher_args = []
	matcher_kwargs = {}
	raises = None
	valid_pairs = []  # List[Tuple[Any, Any]]
	invalid_pairs = []
	inapplicable_constraints = []

	def test_isApplicable_True(self):
		for constraint, _ in self.valid_pairs + self.invalid_pairs:
			self.assertTrue(
				self.matcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertTrue(
				self.matcher(*self.matcher_args, **self.matcher_kwargs).isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_isApplicable_False(self):
		for constraint in self.inapplicable_constraints:
			self.assertFalse(
				self.matcher.isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)
			self.assertFalse(
				self.matcher(*self.matcher_args, **self.matcher_kwargs).isApplicable(constraint),
				msg=f'Failed with constraint {constraint}'
			)

	def test_validate_success(self):
		for constraint, item in self.valid_pairs:
			self.assertTrue(
				self.matcher.validate(item, constraint, default_validator),
				msg=f'Failed with constraint {constraint}, item {item}'
			)
			self.assertTrue(
				self.matcher(*self.matcher_args, **self.matcher_kwargs).validate(item, constraint, default_validator),
				msg=f'Failed with constraint {constraint}, item {item}'
			)

	def test_validate_failure(self):
		for constraint, item in self.invalid_pairs:
			with self.assertRaises(
					self.raises,
					msg=f'Failed with constraint {constraint}, item {item}'
			) as context:
				self.matcher.validate(item, constraint, default_validator)
				self.matcher(*self.matcher_args, **self.matcher_kwargs).validate(item, constraint, default_validator)
			logger.debug(context.exception)

