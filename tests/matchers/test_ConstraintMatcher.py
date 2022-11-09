
import typing
import re
import logging
from simpleschema.matchers import ConstraintMatcher
from tests.matchers import matcher_test_framework

logger = logging.getLogger(__name__)


class TestConstraintMatcher(matcher_test_framework.TestMatcher):
	matcher = ConstraintMatcher
	matcher_args = []
	matcher_kwargs = {}
	raises = NotImplementedError
	valid_pairs = {}
	invalid_pairs = {}
	inapplicable_constraints = [None, typing.Any, '', 'asdf', re.compile(r'.*'), callable]
	items = [None, typing.Any, '', 'asdf', re.compile(r'.*'), callable]

	def test_isApplicable_True(self):
		for constraint in self.inapplicable_constraints:
			with self.assertRaises(
					NotImplementedError,
					msg=f'Failed with constraint {constraint}'
			) as context:
				ConstraintMatcher.isApplicable(constraint)
				ConstraintMatcher().isApplicable(constraint)
			logger.debug(context.exception)

	def test_isApplicable_False(self):
		pass

