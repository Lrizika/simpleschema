
import unittest
from simpleschema.validate import validateItem, validateSchema, isValid
from simpleschema import ObjectSchema
from simpleschema.exceptions import ItemValidationFailure, LiteralMismatch, TypeMismatch, CallableMismatch, ValueMismatch, RegExMismatch
import typing
import logging
import re


logger = logging.getLogger(__name__)


class TestValidateSchema(unittest.TestCase):
	# Pairs of (schema, item)
	valid_schema_pairs = (
		({typing.Any: typing.Any}, {'a': 1}),
	)
	invalid_schema_pairs = (
		({typing.Any: typing.Any}, {}),
	)

	def test_validates_success(self):
		for pair in self.valid_schema_pairs:
			try:
				self.assertTrue(
					validateSchema(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		for pair in self.invalid_schema_pairs:
			self.assertFalse(validateSchema(schema=pair[0], item=pair[1])[0])


class TestIsValid(unittest.TestCase):
	valid_schema_pairs = TestValidateSchema.valid_schema_pairs
	invalid_schema_pairs = TestValidateSchema.invalid_schema_pairs

	def test_validates_success(self):
		for pair in self.valid_schema_pairs:
			try:
				self.assertTrue(
					isValid(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		for pair in self.invalid_schema_pairs:
			try:
				self.assertFalse(
					isValid(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise


class TestValidateObjectSchema(unittest.TestCase):
	test_schema = ObjectSchema({
		'required_method': callable,
		'required_string_attribute': str,
		('required_a_or', 'required_b'): object,
	})

	def test_valid(self):
		class AlwaysValid:
			required_string_attribute = 'string'

			def required_method():
				pass

			def required_b(self):
				pass

		self.assertTrue(validateSchema(AlwaysValid, self.test_schema))
		self.assertTrue(validateSchema(AlwaysValid(), self.test_schema))

	def test_valid_if_instantiated(self):
		class ValidOnlyIfInstantiated:
			def __init__(self):
				self.required_string_attribute = 'different string'

			def required_method():
				pass

			def required_b(self):
				pass

		self.assertFalse(validateSchema(ValidOnlyIfInstantiated, self.test_schema)[0])
		self.assertTrue(validateSchema(ValidOnlyIfInstantiated(), self.test_schema))

	def test_invalid(self):
		class NeverValid:
			required_string_attribute = 123
			required_method = 'not_a_callable'

			def required_b(self):
				pass

		self.assertFalse(validateSchema(NeverValid, self.test_schema)[0])
		self.assertFalse(validateSchema(NeverValid(), self.test_schema)[0])


class TestValidateItem(unittest.TestCase):
	def test_validates_success(self):
		# Pairs of (schema constraint, item)
		valid_schema_pairs = [
			# Validate due to equality
			('asdf', 'asdf'),
			(b'asdf', b'asdf'),
			(None, None),
			(1234, 1234),
			(False, False),
			((), ()),
			(True, 1),
			# Validate due to typing.Any
			(typing.Any, 'asdf'),
			(typing.Any, None),
			(typing.Any, typing.Any),
			(typing.Any, object()),
			# Validate due to regex match
			(re.compile(r'sd'), 'asdf'),
			# Validate due to typing.Literal argument equality
			(typing.Literal[21], 21),
			(typing.Literal['asdf'], 'asdf'),
			# Validate due to recursion into validateSchema
			# For further testing of validateSchema, see TestValidateSchema
			({'key': 'value'}, {'key': 'value', 'extra_key': None}),
			# Validate due to type checking
			(str, 'asdf'),
			(int, 1234),
			(object, object()),
			(tuple, ()),
			(type(None), None),
			(callable, lambda _: True),
			(type, str),
			(typing.Iterable, []),
			# Validate due to truthy callable
			(bool.__call__, 1),
			(lambda v: v, True),
			(lambda v: v > 50, 60),
			(lambda v: not v, False),
			(lambda v: v > '1.0.1', '2.0.0'),
		]

		for pair in valid_schema_pairs:
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


