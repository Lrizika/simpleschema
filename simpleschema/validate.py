
import typing
import logging
import re
import simpleschema
from simpleschema.helper_classes import ObjectSchema
from simpleschema.exceptions import SchemaValidationFailure, ItemValidationFailure, TypeMismatch, LiteralMismatch, IterableMismatch, CallableMismatch, ValueMismatch, RegExMismatch


logger = logging.getLogger(__name__)
sentinel = object()


def is_valid(item: dict, schema: typing.Union[dict, ObjectSchema]) -> bool:
	"""
	Convenience function that returns a bool instead of raising an exception on validation failure.
		See simpleschema.validate for args

	Returns:
		bool: Whether the schema is valid for the item
	"""
	try:
		return validateSchema(item, schema)
	except SchemaValidationFailure:
		return False


def validateSchema(item: dict, schema: typing.Union[dict, ObjectSchema]) -> bool:
	"""
	Validates a dict against a schema.

	Args:
		item (dict): The item to validate against the schema
		schema (dict or ObjectSchema): The schema to validate.
			Format:
			{
				'key': 'value',
				'key2': {
					'key3': 'RequiredValue'
				}
			}
			Items (both keys and values) validate with the following checks:
			- Direct value comparison
			- If the constraint is re.Pattern, check if there is at least one match in the item
			- If the constraint is typing.Literal, compare its value to the value of the item
			- If the constraint is a dictionary, recursively validate the item against the constraint as a schema
			- If the constraint is a type (or type hint, like typing.Iterable), check if the item is an instance of that type
			- If the constraint is iterable, try each value as a constraint against the item. If any validate, the constraint validates.
			- If the constraint is callable, evaluate it against the item

			Note that values are *always* the first item checked. This means that, for example, if a constraint were `typing.Iterable`, it would validate succesfully for both `[1, 2, 3]` and `typing.Iterable`

			If schema is an ObjectSchema, it will be compared against the item's attributes.
			This can be used to, for example, ensure that a class has a specific method,
			or validate that an instance has been assigned an allowed value.
			See simpleschema.ObjectSchema for example usage.

	Raises:
		ValidationFailure: The key or value that has failed to validate, and the reason.

	Returns:
		bool: If the schema validates, returns True.
			Note that this *only* returns True. If the schema fails to validate, we instead raise
			a ValidationFailure, which includes information about the validation failure.
	"""
	logger.debug(f'Validating schema {schema} against item {item}')
	if isinstance(schema, ObjectSchema):
		logger.debug(f'Converting item {item} into dictionary for validation against ObjectSchema')
		item = {key: getattr(item, key) for key in dir(item)}
	for schema_key, schema_val in schema.items():
		if schema_key in item:
			try:
				validateItem(item[schema_key], schema_val)
			except (ItemValidationFailure, SchemaValidationFailure) as e:
				raise SchemaValidationFailure(e)
		else:
			for item_key, item_val in item.items():
				logger.debug(f'Comparing schema key `{schema_key}`, schema value `{schema_val}` against item key `{item_key}`, item value `{item_val}`')
				try:
					validateItem(item_key, schema_key)
					validateItem(item_val, schema_val)
					break
				except (ItemValidationFailure, SchemaValidationFailure) as e:
					logger.debug(e)
			else:
				raise SchemaValidationFailure(f'Schema key `{schema_key}`: schema value `{schema_val}` - No valid key/value pair found in item')
	return True


def validateItem(item_val: typing.Any, schema_val: typing.Any) -> bool:
	"""
	Validates a value against a schema constraint.

	Args:
		item_val (typing.Any): The value to validate
		schema_val (typing.Any): The schema constraint to validate against

	Raises:
		ValidationFailure: If the value does not validate

	Returns:
		bool: If the value validates, returns True
	"""
	logger.debug(f'Validating schema constraint `{schema_val}` against item `{item_val}`')
	if schema_val == item_val:
		return True
	elif schema_val is typing.Any:
		return True
	elif isinstance(schema_val, re.Pattern):
		if schema_val.search(item_val) is not None:
			return True
		raise RegExMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')
	elif typing.get_origin(schema_val) is typing.Literal:
		literal_args = typing.get_args(schema_val)
		if literal_args and literal_args[0] == item_val:
			return True
		raise LiteralMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')
	elif isinstance(schema_val, dict) and isinstance(item_val, dict):
		return validateSchema(item_val, schema_val)
	elif isinstance(schema_val, simpleschema.ObjectSchema):
		return validateSchema(item_val, schema_val)
	elif (
			isinstance(schema_val, type) or
			callable(getattr(schema_val, "__instancecheck__", None))
	):
		if isinstance(item_val, schema_val):
			return True
		raise TypeMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')
	elif isinstance(schema_val, typing.Iterable) and not isinstance(schema_val, (str, bytes)):
		for schema_val_option in schema_val:
			if schema_val_option != schema_val:
				# This check prevents us from infinite recursion with certain items
				# Where an item of the iterable is in and of itself the same iterable
				try:
					validateItem(item_val, schema_val_option)
					return True
				except ItemValidationFailure as e:
					logger.debug(e)
		raise IterableMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')
	elif callable(schema_val):
		if schema_val(item_val):
			return True
		raise CallableMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')
	else:
		raise ValueMismatch(f'Schema constraint `{schema_val}`, item `{item_val}`')



