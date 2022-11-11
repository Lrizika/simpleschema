
import unittest
from tests.validate.pairs import VALID_SCHEMA_PAIRS, INVALID_SCHEMA_PAIRS
from simpleschema.validate import validateSchema, isValid


class TestValidateSchema(unittest.TestCase):
	def test_validates_success(self):
		for pair in VALID_SCHEMA_PAIRS:
			try:
				self.assertTrue(
					validateSchema(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		for pair in INVALID_SCHEMA_PAIRS:
			self.assertFalse(validateSchema(schema=pair[0], item=pair[1])[0])


class TestIsValid(unittest.TestCase):
	def test_validates_success(self):
		for pair in VALID_SCHEMA_PAIRS:
			try:
				self.assertTrue(
					isValid(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		for pair in INVALID_SCHEMA_PAIRS:
			try:
				self.assertFalse(
					isValid(schema=pair[0], item=pair[1]),
				)
			except Exception:
				print(f'Failed with schema {pair[0]}, item {pair[1]}')
				raise

