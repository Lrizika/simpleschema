
import typing
import logging
from simpleschema.helper_classes import ObjectSchema
from simpleschema.exceptions import ValidationFailure


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
	except ValidationFailure:
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
			Keys validate with the following checks:
			- Direct value comparison
			- If the schema key is a type (or type hint, like typing.Iterable), validate against typing.any pairs in the item with a key of that type
			- If the schema key is iterable, try each value for each check
			- If the schema key is callable, validate against typing.any pairs in the item with a key that evaluates to True
			Values use the same validation methods, with the following addition:
			- If the value is a dictionary, recur

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
			validateItem(item[schema_key], schema_val)
		else:
			for item_key, item_val in item.items():
				logger.debug(f'Comparing schema key `{schema_key}`, schema value `{schema_val}` against item key `{item_key}`, item value `{item_val}`')
				try:
					validateItem(item_key, schema_key)
					validateItem(item_val, schema_val)
					break
				except ValidationFailure as e:
					logger.debug(e)
			else:
				raise ValidationFailure(f'Schema key `{schema_key}`: schema value `{schema_val}` - No valid key/value pair found in item')
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
	elif typing.get_origin(schema_val) is typing.Literal:
		literal_args = typing.get_args(schema_val)
		if literal_args and literal_args[0] == item_val:
			return True
		raise ValidationFailure(f'Schema constraint `{schema_val}`, item `{item_val}` - Literal mismatch')
	elif isinstance(schema_val, dict) and isinstance(item_val, dict):
		return validateSchema(item_val, schema_val)
	elif (
			isinstance(schema_val, type) or
			callable(getattr(schema_val, "__instancecheck__", None))
	):
		if isinstance(item_val, schema_val):
			return True
		raise ValidationFailure(f'Schema constraint `{schema_val}`, item `{item_val}` - Type requirement mismatch')
	elif isinstance(schema_val, typing.Iterable) and not isinstance(schema_val, (str, bytes)):
		for schema_val_option in schema_val:
			if schema_val_option != schema_val:
				# This check prevents us from infinite recursion with certain items
				# Where an item of the iterable is in and of itself the same iterable
				try:
					validateItem(item_val, schema_val_option)
					return True
				except ValidationFailure as e:
					logger.debug(e)
		raise ValidationFailure(f'Schema constraint `{schema_val}`, item `{item_val}` - No item values validate for schema options')
	elif callable(schema_val):
		if schema_val(item_val):
			return True
		raise ValidationFailure(f'Schema constraint `{schema_val}`, item `{item_val}` - Function does not validate')
	else:
		raise ValidationFailure(f'Schema constraint `{schema_val}`, item `{item_val}` - Item does not validate')



