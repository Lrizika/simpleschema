

class ObjectSchema(dict):
	"""
	A schema for an object, rather than a dictionary
	ObjectSchema are identical to dicts
	They are used to indicate a schema should be applied to an object

	Example Usage:

my_schema = simpleschema.ObjectSchema({
	'required_method': callable,
	'required_string_attribute': str,
	('required_a_or', 'required_b'): object,
})
class ValidClass:
	required_string_attribute = 'string'
	def required_method():
		pass
	def required_b(self):
		pass
class ValidOnlyIfInstantiated:
	def __init__(self):
		self.required_string_attribute = 'different string'
	def required_method():
		pass
	def required_b(self):
		pass
class InvalidClass:
	required_string_attribute = 123
	required_method = 'not_a_callable'
	def required_b(self):
		pass
simpleschema.is_valid(ValidClass, my_schema)  # True
simpleschema.is_valid(ValidClass(), my_schema)  # True
simpleschema.is_valid(ValidOnlyIfInstantiated, my_schema)  # False
simpleschema.is_valid(ValidOnlyIfInstantiated(), my_schema)  # True
simpleschema.is_valid(InvalidClass, my_schema)  # False
simpleschema.is_valid(InvalidClass(), my_schema)  # False

	"""

	pass
