
import unittest
import typing
import logging
import re
from tests.validate.pairs import VALID_ITEM_PAIRS
from simpleschema.validate import validateItem
from simpleschema.exceptions import ItemValidationFailure, LiteralMismatch, TypeMismatch, CallableMismatch, ValueMismatch, RegExMismatch

logger = logging.getLogger(__name__)


class TestValidateItem(unittest.TestCase):
	def test_validates_success(self):
		for pair in VALID_ITEM_PAIRS:
			try:
				self.assertTrue(
					validateItem(constraint=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema constraint {pair[0]}, item {pair[1]}')
				raise

	def test_regex_mismatch(self):
		schema_pairs = [
			(re.compile(r'ds'), 'asdf'),
		]

		self.validate_failure(schema_pairs, RegExMismatch)

	def test_literal_mismatch(self):
		schema_pairs = [
			(typing.Literal[21], 1),
			(typing.Literal['a'], 1),
		]

		self.validate_failure(schema_pairs, LiteralMismatch)

	def test_type_mismatch(self):
		schema_pairs = [
			(str, 1),
			(int, '1'),
			(typing.Callable, 1),
			(type, 1),
			(str, b'asdf'),
		]

		self.validate_failure(schema_pairs, TypeMismatch)

	def test_callable_mismatch(self):
		schema_pairs = [
			(bool.__call__, 0),
			(lambda v: v > '1.0.1', '1.0.0'),
			(lambda v: not v, True),
		]

		self.validate_failure(schema_pairs, CallableMismatch)

	def test_value_mismatch(self):
		schema_pairs = [
			(object(), object()),  # Noteably not the same object
			(1234, 1),
			(None, 0),
			(0, ()),
			('asdf', 'a'),
			(b'asdf', 'a'),
		]

		self.validate_failure(schema_pairs, ValueMismatch)

	def validate_failure(
			self,
			schema_pairs: typing.List[tuple],
			exception_type: typing.Type[ItemValidationFailure]
	):
		"""
		Iterates through (schema constraint, item) pairs, and verifies that they
		raise the appropriate subtype of ItemValidationFailure

		Args:
			schema_pairs (typing.List[tuple]): Pairs of (schema constraint, item) to validate
			exception_type (typing.Type[ItemValidationFailure]): Subtype it should raise
		"""
		for pair in schema_pairs:
			with self.assertRaises(
					exception_type,
					msg=f'Failed with schema constraint {pair[0]}, item {pair[1]}'
			) as context:
				validateItem(constraint=pair[0], item=pair[1])
			logger.debug(context.exception)



