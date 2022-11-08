
import typing
import re
import simpleschema
from simpleschema.exceptions import RegExMismatch, LiteralMismatch, SchemaValidationFailure, TypeMismatch, IterableMismatch, CallableMismatch


class ConstraintMatcher:
	# Note that while most isApplicable methods are static methods, there is no
	# fundamental reason for this to be true. It is entirely valid for some
	# ConstraintMatchers to define isApplicable as an instance method or even
	# potentially a class method
	@staticmethod
	def isApplicable(constraint):
		raise NotImplementedError('ConstraintMatchers must provide isApplicable and validate methods')

	# See notes regarding isApplicable
	@staticmethod
	def validate(item, constraint):
		raise NotImplementedError('ConstraintMatchers must provide isApplicable and validate methods')


class AnyMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return constraint is typing.Any

	@staticmethod
	def validate(item, constraint):
		return True


class RegExMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return isinstance(constraint, re.Pattern)

	@staticmethod
	def validate(item, constraint):
		try:
			if constraint.search(item) is not None:
				return True
		except TypeError as e:
			raise RegExMismatch(constraint, item, child_exception=e)
		raise RegExMismatch(constraint, item)


class LiteralMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return typing.get_origin(constraint) is typing.Literal

	@staticmethod
	def validate(item, constraint):
		literal_args = typing.get_args(constraint)
		if literal_args and literal_args[0] == item:
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
			isinstance(constraint, type) or
			callable(getattr(constraint, "__instancecheck__", None))
		)

	@staticmethod
	def validate(item, constraint):
		if isinstance(item, constraint):
			return True
		raise TypeMismatch(constraint, item)


# TODO: This probably needs to live in SchemaValidator
# class IterableMatcher(ConstraintMatcher):
# 	@staticmethod
# 	def isApplicable(constraint):
# 		return (
# 			isinstance(constraint, typing.Iterable) and not
# 			isinstance(constraint, (str, bytes))
# 		)

# 	@staticmethod
# 	def validate(item, constraint):
# 		for constraint_option in constraint:
# 			if constraint_option != constraint:
# 				# This check prevents us from infinite recursion with certain items
# 				# Where an item of the iterable is in and of itself the same iterable
# 				try:
# 					validateItem(item, constraint_option)
# 					return True
# 				except ItemValidationFailure as e:
# 					logger.debug(e)
# 		raise IterableMismatch(constraint, item)


class CallableMatcher(ConstraintMatcher):
	@staticmethod
	def isApplicable(constraint):
		return callable(constraint)

	@staticmethod
	def validate(item, constraint):
		if constraint(item):
			return True
		raise CallableMismatch(constraint, item)

