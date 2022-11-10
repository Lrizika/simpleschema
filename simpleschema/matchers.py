
import typing
import re
import simpleschema
from simpleschema.exceptions import RegExMismatch, LiteralMismatch, SchemaValidationFailure, TypeMismatch, CallableMismatch


class ConstraintMatcher:
	# Note that while most isApplicable methods are static methods, there is no
	# fundamental reason for this to be true. It is entirely valid for some
	# ConstraintMatchers to define isApplicable as an instance method or even
	# potentially a class method
	@staticmethod
	def isApplicable(constraint):
		raise NotImplementedError('ConstraintMatchers must provide isApplicable method')

	# See notes regarding isApplicable
	@staticmethod
	def validate(item, constraint):
		raise NotImplementedError('ConstraintMatchers must provide validate method')


class AnyMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return (
			constraint is typing.Any or
			constraint is simpleschema.constraints.Any or
			isinstance(constraint, simpleschema.constraints.Any)
		)

	@staticmethod
	def validate(item, constraint):
		return True


class RegExMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return isinstance(constraint, (re.Pattern, simpleschema.constraints.RegEx))

	@staticmethod
	def validate(item, constraint):
		try:
			if constraint.search(item) is not None:
				return True
		except TypeError as e:
			raise RegExMismatch(constraint, item) from e
		raise RegExMismatch(constraint, item)


class LiteralMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return (
			typing.get_origin(constraint) is typing.Literal or
			isinstance(constraint, simpleschema.constraints.Literal)
		)

	@staticmethod
	def validate(item, constraint):
		if typing.get_origin(constraint) is typing.Literal:
			literal_args = typing.get_args(constraint)
			if literal_args and literal_args[0] == item:
				return True
		elif isinstance(constraint, simpleschema.constraints.Literal):
			if constraint.obj == item:
				return True
		raise LiteralMismatch(constraint, item)


class ChildSchemaMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return isinstance(constraint, dict)

	@staticmethod
	def validate(item, constraint):
		child_schema_result = simpleschema.validate.validateSchema(item, constraint)
		if child_schema_result[0] is True:
			return True
		raise SchemaValidationFailure(constraint, child_schema_result=child_schema_result)


class TypeMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return (
			isinstance(constraint, (type, simpleschema.constraints.Type)) or
			callable(getattr(constraint, "__instancecheck__", None))
		)

	@staticmethod
	def validate(item, constraint):
		if isinstance(constraint, simpleschema.constraints.Type):
			constraint = constraint.obj
		if isinstance(item, constraint):
			return True
		raise TypeMismatch(constraint, item)


class CallableMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return callable(constraint) or isinstance(constraint, simpleschema.constraints.Callable)

	@staticmethod
	def validate(item, constraint):
		if constraint(item):
			return True
		raise CallableMismatch(constraint, item)

