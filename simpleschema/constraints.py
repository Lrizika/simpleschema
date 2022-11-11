
import re


class Constraint:
	"""
	Used for wrapping constraints
	This can be useful for explicitly declaring constraints
	that might otherwise be valid for multiple constraint types
	E.G. a class with a __call__ method is both a viable type
	constraint and a callable constraint
	Wrapping said class in a Type constraint ensures it is tested
	as a type, no matter the resolution order of the SchemaValidator
	"""
	def __init__(self, obj: object) -> None:
		self.obj = obj

	def __hash__(self) -> int:
		return hash(hash(self.obj) + hash(type(self)))

	def __repr__(self) -> str:
		return f'{type(self).__name__}<{repr(self.obj)}>'

	def __str__(self) -> str:
		return f'{type(self).__name__}<{str(self.obj)}>'


class Literal(Constraint):
	"""
	Used for wrapping literal objects (e.g. `callable`)
	"""
	pass


class Callable(Constraint):
	def __call__(self, *args, **kwargs):
		return self.obj(*args, **kwargs)


class Any(Constraint):
	def __init__(self) -> None:
		raise TypeError(f'{type(self)} should not be initialized.')


class Type(Constraint):
	pass


class RegEx(Constraint):
	def __init__(self, obj: object) -> None:
		if isinstance(obj, str):
			obj = re.compile(obj)
		super().__init__(obj)
		self.search = obj.search

