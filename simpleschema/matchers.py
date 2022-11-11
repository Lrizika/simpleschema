
import typing
import re
from simpleschema import constraints
from simpleschema.exceptions import RegExMismatch, LiteralMismatch, SchemaValidationFailure, TypeMismatch, CallableMismatch


class ConstraintMatcher:
	# Note that while most isApplicable methods are static methods, there is no
	# fundamental reason for this to be true. It is entirely valid for some
	# ConstraintMatchers to define isApplicable as an instance method or even
	# potentially a class method
	@staticmethod
	def isApplicable(
			constraint: typing.Union[constraints.Constraint, typing.Any],
	) -> bool:
		"""
		Returns whether a ConstraintMatcher can be applied to a given constraint
		A SchemaValidator checks each of its ConstraintMatchers' isApplicable methods
		and validates with the first relevant one. This is why order of ConstraintMatchers
		is important while initializing oyur SchemaValidator.

		Args:
			constraint (
				typing.Union[constraints.Constraint, typing.Any]
			): The constraint to check the ConstraintMatcher's applicability to

		Returns:
			bool: Whether the ConstraintMatcher can be applied
		"""
		raise NotImplementedError('ConstraintMatchers must provide isApplicable method')

	# See notes regarding isApplicable
	@staticmethod
	def validate(
			item: typing.Any,
			constraint: typing.Union[constraints.Constraint, typing.Any],
			validator,
	) -> bool:
		"""
		Returns True if the item validates for a constraint with this ConstraintMatcher,
		or raises the appropriate ItemValidationFailure if it does not validate
		This should only ever be called after isApplicable has returned True for the constraint

		Args:
			item (typing.Any): The item to validate
			constraint (
				typing.Union[constraints.Constraint, typing.Any]
			): The constraint to validate against
			validator (simpleschema.validate.SchemaValidator): The validator to use, if relevant
				This is important for things like ChildSchemaMatcher, where the validator must recurse

		Raises:
			ItemValidationFailure: If the item does not validate

		Returns:
			bool: Always True if the item validates
		"""
		raise NotImplementedError('ConstraintMatchers must provide validate method')


class AnyMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return (
			constraint is typing.Any or
			constraint is constraints.Any or
			isinstance(constraint, constraints.Any)
		)

	@staticmethod
	def validate(item, constraint, validator):
		return True


class RegExMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return isinstance(constraint, (re.Pattern, constraints.RegEx))

	@staticmethod
	def validate(item, constraint, validator):
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
			isinstance(constraint, constraints.Literal)
		)

	@staticmethod
	def validate(item, constraint, validator):
		if typing.get_origin(constraint) is typing.Literal:
			literal_args = typing.get_args(constraint)
			if literal_args and literal_args[0] == item:
				return True
		elif isinstance(constraint, constraints.Literal):
			if constraint.obj == item:
				return True
		raise LiteralMismatch(constraint, item)


class ChildSchemaMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return isinstance(constraint, dict)

	@staticmethod
	def validate(item, constraint, validator):
		child_schema_result = validator.validate(item, constraint)
		if child_schema_result[0] is True:
			return True
		raise SchemaValidationFailure(constraint, child_schema_result=child_schema_result)


class TypeMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return (
			isinstance(constraint, (type, constraints.Type)) or
			callable(getattr(constraint, "__instancecheck__", None))
		)

	@staticmethod
	def validate(item, constraint, validator):
		if isinstance(constraint, constraints.Type):
			constraint = constraint.obj
		if isinstance(item, constraint):
			return True
		raise TypeMismatch(constraint, item)


class CallableMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return callable(constraint) or isinstance(constraint, constraints.Callable)

	@staticmethod
	def validate(item, constraint, validator):
		if constraint(item):
			return True
		raise CallableMismatch(constraint, item)

