
import typing
import logging
from simpleschema.schema_types import ObjectSchema
from simpleschema.exceptions import ConstraintException, SchemaValidationFailure, ItemValidationFailure, ValueMismatch
from simpleschema.matchers import ConstraintMatcher, AnyMatcher, RegExMatcher, LiteralMatcher, ChildSchemaMatcher, TypeMatcher, CallableMatcher
from simpleschema.constraints import Constraint

logger = logging.getLogger(__name__)


class SchemaValidator:
	def __init__(
			self,
			matcherClasses: typing.List[typing.Type[ConstraintMatcher]] = [
				AnyMatcher, RegExMatcher, LiteralMatcher, ChildSchemaMatcher, TypeMatcher, CallableMatcher
			]
	) -> None:
		self.matchers = [matcher() for matcher in matcherClasses]

	def get_matcher(
			self,
			constraint: typing.Union[Constraint, typing.Any],
	) -> ConstraintMatcher:
		for matcher in self.matchers:
			if matcher.isApplicable(constraint):
				return matcher
		raise ConstraintException(f'Invalid constraint `{constraint}`')

	def validateItem(
			self,
			item: typing.Any,
			constraint: typing.Union[Constraint, typing.Any],
	) -> bool:
		if item == constraint:
			return True
		try:
			matcher = self.get_matcher(constraint)
		except ConstraintException as e:
			raise ValueMismatch(constraint, item) from e
		return matcher.validate(item, constraint, self)

	def validate(
			self,
			item: dict,
			schema: dict,
	) -> typing.Tuple[
			bool,
			typing.List[typing.Union[
				ItemValidationFailure,
				SchemaValidationFailure
			]]
	]:
		validation_failures = []
		validation_status = True

		logger.debug(f'Validating schema {schema} against item {item}')
		if isinstance(schema, ObjectSchema):
			logger.debug(f'Converting item {item} into dictionary for validation against ObjectSchema')
			item = {key: getattr(item, key) for key in dir(item)}
		for schema_key, schema_val in schema.items():
			if schema_key in item:
				try:
					self.validateItem(item[schema_key], schema_val)
				except (ItemValidationFailure, SchemaValidationFailure) as e:
					validation_status = False
					new_exception = SchemaValidationFailure(schema_key)
					new_exception.__cause__ = e
					validation_failures.append(new_exception)
			else:
				for item_key, item_val in item.items():
					logger.debug(f'Comparing schema key `{schema_key}`, schema value `{schema_val}` against item key `{item_key}`, item value `{item_val}`')
					try:
						self.validateItem(item_key, schema_key)
						self.validateItem(item_val, schema_val)
						break
					except (ItemValidationFailure, SchemaValidationFailure) as e:
						logger.debug(e)
				else:
					validation_status = False
					validation_failures.append(SchemaValidationFailure(schema_key))
		return (validation_status, validation_failures)


default_validator = SchemaValidator()


def validateSchema(
		item: dict,
		schema: typing.Union[dict, ObjectSchema]
) -> typing.Tuple[
		bool,
		typing.List[typing.Union[
			SchemaValidationFailure,
			ItemValidationFailure
		]]
]:
	return default_validator.validate(item, schema)


def isValid(item, schema) -> bool:
	return validateSchema(item, schema)[0]


validateItem = default_validator.validateItem
