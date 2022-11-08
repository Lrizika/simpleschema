

class SimpleSchemaException(Exception):
	"""
	Base class for all custom exceptions in this module
	"""
	pass


class ValidationFailure(SimpleSchemaException):
	"""
	Base class for exceptions raised when something does not validate
	"""
	pass


class SchemaValidationFailure(ValidationFailure):
	"""
	Raised when a schema does not validate
	"""
	def __init__(self, schema_key, *args, **kwargs):
		super().__init__()
		self.schema_key = schema_key
		self.args = args
		self.kwargs = kwargs

	def __repr__(self):
		result = f'{type(self).__name__}<schema_key: `{self.schema_key}`'
		if self.args:
			result += f', args: `{self.args}`'
		if self.kwargs:
			result += f', kwargs: `{self.kwargs}`'
		result += '>'
		return result


class ItemValidationFailure(ValidationFailure):
	"""
	Raised when an item does not validate, and there is not
	a more relevant exception to raise
	"""
	def __init__(self, constraint, item, *args, **kwargs):
		super().__init__()
		self.constraint = constraint
		self.item = item
		self.args = args
		self.kwargs = kwargs

	def __repr__(self):
		result = f'{type(self).__name__}<constraint: `{self.constraint}`, item: `{self.item}`'
		if self.args:
			result += f', args: `{self.args}`'
		if self.kwargs:
			result += f', kwargs: `{self.kwargs}`'
		result += '>'
		return result


class RegExMismatch(ItemValidationFailure):
	"""
	Raised when an item does not match a re.Pattern constraint
	"""
	pass


class LiteralMismatch(ItemValidationFailure):
	"""
	Raised when an item does not match a typing.Literal constraint
	"""
	pass


class TypeMismatch(ItemValidationFailure):
	"""
	Raised when an item does not match a type constraint
	"""
	pass


class IterableMismatch(ItemValidationFailure):
	"""
	Raised when an item does not match any constraints in an iterable of constraints
	"""
	pass


class CallableMismatch(ItemValidationFailure):
	"""
	Raised when a callable constraint does not evaluate to truthy for an item
	"""
	pass


class ValueMismatch(ItemValidationFailure):
	"""
	Raised when a constraint does not match to any value in the item, and no alternative
	validation patterns could be applied
	"""
	pass


class ConstraintException(SimpleSchemaException):
	"""
	Raised when a constraint does not match any validation patterns
	"""
	pass

