
import unittest
from simpleschema.validate import validateSchema
from simpleschema import ObjectSchema
import logging

logger = logging.getLogger(__name__)


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


