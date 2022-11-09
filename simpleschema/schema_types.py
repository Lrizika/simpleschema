

class Literal:
	"""
	Used for wrapping literal objects (e.g. `callable`)
	that would otherwise be valid constraints
	"""
	def __init__(self, obj: object) -> None:
		self.obj = obj

	def __hash__(self) -> int:
		return hash(hash(self.obj) + hash(type(self)))

	def __repr__(self) -> str:
		return f'{type(self).__name__}<{repr(self.obj)}>'

	def __str__(self) -> str:
		return f'{type(self).__name__}<{str(self.obj)}>'


class Schema(dict):
	pass


class DictSchema(Schema):
	pass


class ObjectSchema(Schema):
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
simpleschema.isValid(ValidClass, my_schema)  # True
simpleschema.isValid(ValidClass(), my_schema)  # True
simpleschema.isValid(ValidOnlyIfInstantiated, my_schema)  # False
simpleschema.isValid(ValidOnlyIfInstantiated(), my_schema)  # True
simpleschema.isValid(InvalidClass, my_schema)  # False
simpleschema.isValid(InvalidClass(), my_schema)  # False

	"""

	pass
