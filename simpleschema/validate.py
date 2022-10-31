
from typing import Any, Iterable
import logging


logger = logging.getLogger(__name__)
sentinel = object()


def is_valid(item: dict, schema: dict) -> bool:
	"""
	Convenience function that returns a bool instead of raising an exception on validation failure.
		See simpleschema.validate for args

	Returns:
		bool: Whether the schema is valid for the item
	"""
	try:
		return validateSchema(item, schema)
	except ValueError:
		return False


def validateSchema(item: dict, schema: dict) -> bool:
	"""
	Validates a dict against a schema.

	Args:
		item (dict): The item to validate against the schema
		schema (dict): The schema to validate.
			Format:
			{
				'key': 'value',
				'key2': {
					'key3': 'RequiredValue'
				}
			}
			Keys validate with the following checks:
			- Direct value comparison
			- If the schema key is a type (or type hint, like typing.Iterable), validate against any pairs in the item with a key of that type
			- If the schema key is iterable, try each value for each check
			- If the schema key is callable, validate against any pairs in the item with a key that evaluates to True
			Values use the same validation methods, with the following addition:
			- If the value is a dictionary, recur

	Raises:
		ValueError: The key or value that has failed to validate, and the reason.

	Returns:
		bool: If the schema validates, returns True.
			Note that this *only* returns True. If the schema fails to validate, we instead raise
			a ValueError, which includes information about the validation failure.
	"""
	for schema_key, schema_val in schema.items():
		if schema_key in item:
			validateItem(item[schema_key], schema_val)
		else:
			for item_key, item_val in item.items():
				logger.debug(f'Comparing schema key {schema_key}, schema value {schema_val} against item key {item_key}, item value {item_val}')
				try:
					validateItem(item_key, schema_key)
					validateItem(item_val, schema_val)
					break
				except ValueError as e:
					logger.debug(e)
			else:
				raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No valid key/value pair found in item')
	return True


def validateItem(item_val: Any, schema_val: Any) -> bool:
	"""
	Validates a value against a schema constraint.

	Args:
		item_val (Any): The value to validate
		schema_val (Any): The schema constraint to validate against

	Raises:
		ValueError: If the value does not validate

	Returns:
		bool: If the value validates, returns True
	"""
	if schema_val == item_val:
		logger.debug(f'Schema constraint {schema_val}, item value {item_val} - Validation success')
		return True
	elif isinstance(schema_val, dict) and isinstance(item_val, dict):
		return validateSchema(item_val, schema_val)
	elif (
			isinstance(schema_val, type) or
			callable(getattr(schema_val, "__instancecheck__", None))
	):
		if isinstance(item_val, schema_val):
			logger.debug(f'Schema constraint {schema_val}, item value {item_val} - Validation success')
			return True
		else:
			raise ValueError(f'Schema constraint {schema_val}, item value {item_val} - Type requirement mismatch')
	elif isinstance(schema_val, Iterable):
		for schema_val_option in schema_val:
			if schema_val_option != schema_val:
				# This check prevents us from infinite recursion with items like strings
				# Where an item of the iterable is in and of itself iterable
				try:
					validateItem(item_val, schema_val_option)
					return True
				except ValueError as e:
					logger.debug(e)
		else:
			raise ValueError(f'Schema constraint {schema_val}, item value {item_val} - No item values validate for schema options')
	elif callable(schema_val):
		if schema_val(item_val):
			logger.debug(f'Schema constraint {schema_val}, item value {item_val} - Validation success')
			return True
		else:
			raise ValueError(f'Schema constraint {schema_val}, item value {item_val} - Function does not validate')
	else:
		raise ValueError(f'Schema constraint {schema_val}, item value {item_val} - Item does not validate')



