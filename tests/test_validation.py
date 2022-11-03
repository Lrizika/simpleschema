
import unittest
from simpleschema.validate import validateItem, validateSchema, is_valid
from simpleschema import ObjectSchema
from simpleschema.exceptions import SchemaValidationFailure, LiteralMismatch, TypeMismatch
from simpleschema.exceptions import ItemValidationFailure  # TODO: Remove this
import typing
import logging
import sys


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
			with self.assertRaises(
					SchemaValidationFailure,
					msg=f'Failed with schema {pair[0]}, item {pair[1]}'
			) as context:
				validateSchema(schema=pair[0], item=pair[1])
			logger.debug(context.exception)


class TestIsValid(unittest.TestCase):
	valid_schema_pairs = TestValidateSchema.valid_schema_pairs
	invalid_schema_pairs = TestValidateSchema.invalid_schema_pairs

	def test_validates_success(self):
		for pair in self.valid_schema_pairs:
			try:
				self.assertTrue(
					is_valid(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		for pair in self.invalid_schema_pairs:
			try:
				self.assertFalse(
					is_valid(schema=pair[0], item=pair[1]),
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

		with self.assertRaises(SchemaValidationFailure) as context:
			validateSchema(ValidOnlyIfInstantiated, self.test_schema)
		logger.debug(context.exception)
		self.assertTrue(validateSchema(ValidOnlyIfInstantiated(), self.test_schema))

	def test_invalid(self):
		class NeverValid:
			required_string_attribute = 123
			required_method = 'not_a_callable'

			def required_b(self):
				pass

		with self.assertRaises(SchemaValidationFailure) as context:
			validateSchema(NeverValid, self.test_schema)
		logger.debug(context.exception)
		with self.assertRaises(SchemaValidationFailure) as context:
			validateSchema(NeverValid(), self.test_schema)
		logger.debug(context.exception)


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
			# Validate due to valid option in iterable
			((1234, 'asdf', callable), lambda _: True),
			([1234, 4321, 1111], 4321),
			((1234, 'asdf', callable), 'asdf'),
			(iter(['asdf', 'fdsa', 'ghjk']), 'ghjk'),
			((v for v in (1234, 4321, 1111)), 4321),
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
					validateItem(schema_val=pair[0], item_val=pair[1]),
				)
			except Exception:
				print(f'Failed with schema constraint {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		invalid_schema_pairs = [
			# Invalid equalities
			(object(), object()),  # Noteably not the same object
			(1234, 1),
			(None, 0),
			((), 0),
			('asdf', 'a'),
			(b'asdf', 'a'),
			# Invalid typing.Literal
			(typing.Literal[21], 1),
			(typing.Literal['a'], 1),
			# Invalid types
			(str, 1),
			(int, '1'),
			(callable, 1),
			(type, 1),
			(str, b'asdf'),
			# Missing option in iterable
			([1, 2], 3),
			((1, 2, 3), '2'),
			((), None),
			# Falsy callable
			(bool.__call__, 0),
			(lambda v: v > '1.0.1', '1.0.0'),
			(lambda v: not v, True),
		]

		for pair in invalid_schema_pairs:
			with self.assertRaises(
					ItemValidationFailure,
					msg=f'Failed with schema constraint {pair[0]}, item {pair[1]}'
			) as context:
				validateItem(schema_val=pair[0], item_val=pair[1])
			logger.debug(context.exception)


if __name__ == '__main__':
	if ('-vv' in sys.argv) or ('--very-verbose' in sys.argv):
		logging.basicConfig(level=logging.DEBUG, format='    %(funcName)s %(message)s')
	unittest.main()
