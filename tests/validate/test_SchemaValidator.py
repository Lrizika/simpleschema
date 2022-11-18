
import unittest
from tests.validate.pairs import VALID_SCHEMA_PAIRS, INVALID_SCHEMA_PAIRS
from simpleschema.validate import SchemaValidator
from simpleschema.matchers import AnyMatcher, RegExMatcher, LiteralMatcher, ChildSchemaMatcher, TypeMatcher, CallableMatcher
from simpleschema.exceptions import SchemaValidationFailure, ItemValidationFailure


class TestValidateSchema(unittest.TestCase):
	def test_validates_success(self):
		validator = SchemaValidator([AnyMatcher, RegExMatcher, LiteralMatcher, ChildSchemaMatcher, TypeMatcher, CallableMatcher])
		for pair in VALID_SCHEMA_PAIRS:
			try:
				self.assertTrue(
					validator.validate(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		validator = SchemaValidator([AnyMatcher, RegExMatcher, LiteralMatcher, ChildSchemaMatcher, TypeMatcher, CallableMatcher])
		for pair in INVALID_SCHEMA_PAIRS:
			result = validator.validate(schema=pair[0], item=pair[1])
			self.assertFalse(result[0])
			for e in result[1]:
				self.assertIsInstance(e, (SchemaValidationFailure, ItemValidationFailure))

