

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
	def __init__(self, schema_key, *args, causes=[], **kwargs):
		super().__init__(*args)
		self.schema_key = schema_key
		self.causes = causes
		self.kwargs = kwargs

	def __repr__(self):
		result = f'{type(self).__name__}<schema_key: `{self.schema_key}`'
		if self.args:
			result += f', args: `{self.args}`'
		if self.kwargs:
			result += f', kwargs: `{self.kwargs}`'
		if self.__cause__:
			result += f', cause: `\n\t{self.__cause__}\n`'
		if self.causes:
			result += ', causes: `['
			for cause in self.causes:
				result += f'\n\t{cause}'
			result += '\n]`'
		result += '>'
		return result

	__str__ = __repr__


class NoValidKeyValuePairs(SchemaValidationFailure):
	"""
	Raised when no pair of item key/value pairs are valid
	"""
	pass


class ItemValidationFailure(ValidationFailure):
	"""
	Raised when an item does not validate, and there is not
	a more relevant exception to raise
	"""
	def __init__(self, constraint, item, *args, **kwargs):
		super().__init__(*args)
		self.constraint = constraint
		self.item = item
		self.kwargs = kwargs

	def __repr__(self):
		result = f'{type(self).__name__}<constraint: `{self.constraint}`, item: `{self.item}`'
		if self.args:
			result += f', args: `{self.args}`'
		if self.kwargs:
			result += f', kwargs: `{self.kwargs}`'
		if self.__cause__:
			result += f', cause: `{self.__cause__}`'
		result += '>'
		return result

	__str__ = __repr__


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

