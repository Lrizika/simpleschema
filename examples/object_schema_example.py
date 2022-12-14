
import simpleschema

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


print(
	'simpleschema.isValid(ValidClass, my_schema)',
	simpleschema.isValid(ValidClass, my_schema)
)  # True
print(
	'simpleschema.isValid(ValidClass(), my_schema)',
	simpleschema.isValid(ValidClass(), my_schema)
)  # True
print(
	'simpleschema.isValid(ValidClass(), my_schema)',
	simpleschema.isValid(ValidClass(), my_schema)
)  # True
print(
	'simpleschema.isValid(ValidOnlyIfInstantiated, my_schema)',
	simpleschema.isValid(ValidOnlyIfInstantiated, my_schema)
)  # False
print(
	'simpleschema.isValid(ValidOnlyIfInstantiated(), my_schema)',
	simpleschema.isValid(ValidOnlyIfInstantiated(), my_schema)
)  # True
print(
	'simpleschema.isValid(InvalidClass, my_schema)',
	simpleschema.isValid(InvalidClass, my_schema)
)  # False
print(
	'simpleschema.isValid(InvalidClass(), my_schema)',
	simpleschema.isValid(InvalidClass(), my_schema)
)  # False

