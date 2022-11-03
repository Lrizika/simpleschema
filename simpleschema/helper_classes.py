

class ObjectSchema(dict):
	"""
	A schema for an object, rather than a dictionary
	ObjectSchema are identical to dicts
	They are used to indicate a schema should be applied to an object

	Example Usage:
		>>> my_schema = simpleschema.ObjectSchema({
		...     'required_method': callable,
		...     'required_string_attribute': str,
		...     ('required_a_or', 'required_b'): object,
		... })
		>>> class ValidClass:
		...     required_string_attribute = 'string'
		...     def required_method():
		...             pass
		...     def required_b(self):
		...             pass
		>>> class InvalidClass:
		...     required_string_attribute = 123
		...     def required_method():
		...             pass
		...     def required_b(self):
		...             pass
		>>> simpleschema.validate(ValidClass, my_schema)
		True
		>>> simpleschema.validate(InvalidClass, my_schema)
		Traceback (most recent call last):
		File "<stdin>", line 1, in <module>
		File "/var/git-shared/simpleschema/simpleschema/validate.py", line 61, in validateSchema
			validateItem(item[schema_key], schema_val)
		File "/var/git-shared/simpleschema/simpleschema/validate.py", line 108, in validateItem
			raise ValueError(f'Schema constraint `{schema_val}`, item `{item_val}` - Type requirement mismatch')
		ValueError: Schema constraint `<class 'str'>`, item `123` - Type requirement mismatch
	"""

	pass
