
from typing import Any, Iterable
import logging


sentinel = object()


# def validateSchema(
# 		item: dict,
# 		schema: dict,
# 		schema_key: Any = sentinel,
# 		schema_val: Any = sentinel,
# ) -> bool:
# 	"""
# 	Validates a dict against a schema.

# 	Args:
# 		item (dict): The item to validate against the schema
# 		schema (dict): The schema to validate.
# 			Format:
# 			{
# 				'key': 'value',
# 				'key2': {
# 					'key3': 'RequiredValue'
# 				}
# 			}
# 			Keys validate with the following checks:
# 			- Direct value comparison
# 			- If the schema key is a type (or type hint, like typing.Iterable), validate against any pairs in the item with a key of that type
# 			- If the schema key is iterable, try each value for each check
# 			- If the schema key is callable, validate against any pairs in the item with a key that evaluates to True
# 			Values use the same validation methods, with the following addition:
# 			- If the value is a dictionary, recur
# 		schema_key (Any, optional): Internal use primarily. If set, only validates the schema for that specific key
# 		schema_val (Any, optional): Internal use primarily. If set, validates for that value instead of getting the value from the main schema dict. Generally only used for passing through the value on iterable schema keys, where we can't access schema[schema_key] (since schema_key is only one option of an iterable, and thus does not exist in schema.)

# 	Raises:
# 		ValueError: The key or value that has failed to validate, and the reason.

# 	Returns:
# 		bool: If the schema validates, returns True. Otherwise, raises a ValueError.
# 			If neither of these happens, something has gone *very* awry.
# 	"""
# 	# Returns True if successful, raises ValueError if not
# 	if schema_key is sentinel:
# 		for schema_key in schema:
# 			validateSchema(item, schema, schema_key, schema[schema_key])
# 		return True
# 	else:
# 		if schema_val is sentinel:
# 			schema_val = schema[schema_key]
# 		if schema_key in item:
# 			validateItem(item[schema_key], schema_val)
# 		elif (
# 				isinstance(schema_key, type) or
# 				callable(getattr(schema_key, "__instancecheck__", None))
# 		):
# 			# If the schema key is a class or otherwise supports isinstance()
# 			# We check if any keys in the item are an instance of the class
# 			for item_key in item:
# 				if isinstance(item_key, schema_key):
# 					try:
# 						validateItem(item[item_key], schema_val)
# 						return True
# 					except ValueError:
# 						pass
# 			else:
# 				raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No item values validate for keys with type match')
# 		elif isinstance(schema_key, Iterable):
# 			for schema_key_option in schema_key:
# 				try:
# 					if schema_key in schema:
# 						# Prevent recursion in schema keys
# 						validateSchema(item, schema, schema_key_option, schema[schema_key])
# 						return True
# 				except ValueError:
# 					pass
# 			else:
# 				raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No item values validate for keys in iterable')
# 		elif callable(schema_key):
# 			for item_key in item:
# 				if schema_key(item_key):
# 					try:
# 						validateItem(item[item_key], schema_val)
# 						return True
# 					except ValueError:
# 						pass
# 			else:
# 				raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No item values validate for keys with function match')
# 		else:
# 			raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No valid key found in item')


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
		bool: If the schema validates, returns True. Otherwise, raises a ValueError.
			If neither of these happens, something has gone *very* awry.
	"""
	for schema_key, schema_val in schema.items():
		if schema_key in item:
			validateItem(item[schema_key], schema_val)
		else:
			for item_key, item_val in item.items():
				try:
					validateItem(item_key, schema_key)
					validateItem(item_val, schema_val)
					break
				except ValueError as e:
					logging.info(e)
			else:
				raise ValueError(f'Schema key {schema_key}: schema value {schema_val} - No valid key/value pair found in item')
	return True


def validateItem(item_val: Any, schema_val: Any) -> bool:
	"""
	Validates a value against the schema value for that key.

	Args:
		item_val (Any): The value to validate
		schema_val (Any): The schema value to validate against

	Raises:
		ValueError: If the value does not validate

	Returns:
		bool: If the value validates, returns True
	"""
	if schema_val == item_val:
		return True
	elif isinstance(schema_val, dict) and isinstance(item_val, dict):
		return validateSchema(item_val, schema_val)
	elif (
			isinstance(schema_val, type) or
			callable(getattr(schema_val, "__instancecheck__", None))
	):
		if isinstance(item_val, schema_val):
			return True
		else:
			raise ValueError(f'Schema value {schema_val}, item value {item_val} - Type requirement mismatch')
	elif isinstance(schema_val, Iterable):
		for schema_val_option in schema_val:
			if schema_val_option != schema_val:
				# This check prevents us from infinite recursion with items like strings
				# Where an item of the iterable is in and of itself iterable
				try:
					validateItem(item_val, schema_val_option)
					return True
				except ValueError as e:
					logging.info(e)
		else:
			raise ValueError(f'Schema value {schema_val}, item value {item_val} - No item values validate for schema options')
	elif callable(schema_val):
		if schema_val(item_val):
			return True
		else:
			raise ValueError(f'Schema value {schema_val}, item value {item_val} - Function does not validate')
	else:
		raise ValueError(f'Schema value {schema_val}, item value {item_val} - Item does not validate')



