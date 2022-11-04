
# simpleschema

**simpleschema** is a library for validating dicts or objects to ensure they have a given structure. A use case for this might be to verify integrity of received data, parse event types based on a specification, or ensure arbitrary objects provide certain required methods.

It is intended to provide advanced validation methods with a simple, no-fuss interface.

Validation constraints can be a specific value, a type (or typelike), a set of options, a user-defined validation callable, or even another schema. See [Validation Details](#Validation-Details) or `help(simpleschema.validateSchema)` for more information.

`simpleschema.validateSchema` validates an item against a schema, returning `True` or raising a `simpleschema.SchemaValidationFailure` if it fails to validate. `simpleschema.is_valid` provides a convenience wrapper to `validateSchema`, instead returning `False` on validation failure.

## Example Usage:
```python
import simpleschema

my_schema = {
	'method': ['GET', 'POST'],
	'timestamp': int,
	'version': lambda v: v >= '1.0.0',
}

my_item = {
	'timestamp': 1667515052,
	'method': 'GET',
	'status': 200,
	'json': {
		'key': 'value'
	},
	'version': '2.1.1',
}

bad_item = {
	'timestamp': '1667515052',
	'method': 'PUT',
	'version': '0.1.9',
}

simpleschema.is_valid(item=my_item, schema=my_schema)  # True
simpleschema.is_valid(item=bad_item, schema=my_schema)  # False
```

Schemata can also be used to validate object structure:
```python
import simpleschema

my_schema = simpleschema.ObjectSchema({
	'required_method': callable,
	'required_string_attribute': str,
	('required_a_or', 'required_b'): object,
})

class ValidClass:
	required_string_attribute = 'string'
	def required_method():
		pass
	def required_b(self):
		pass

class ValidOnlyIfInstantiated:
	def __init__(self):
		self.required_string_attribute = 'different string'
	def required_method():
		pass
	def required_b(self):
		pass

class InvalidClass:
	required_string_attribute = 123
	required_method = 'not_a_callable'
	def required_b(self):
		pass

simpleschema.is_valid(ValidClass, my_schema)  # True
simpleschema.is_valid(ValidClass(), my_schema)  # True
simpleschema.is_valid(ValidOnlyIfInstantiated, my_schema)  # False
simpleschema.is_valid(ValidOnlyIfInstantiated(), my_schema)  # True
simpleschema.is_valid(InvalidClass, my_schema)  # False
simpleschema.is_valid(InvalidClass(), my_schema)  # False
```


## Installation

`pip install simpleschema`

## Validation Details

Keys-value pairs in the schema are compared as constraints against each pair in the item, by the following methods, in order:
- Direct value comparison
- If the constraint is typing.Literal, compare its value to the value of the item
- If the constraint is a dictionary, recursively validate the item against the constraint as a schema
- If the constraint is a type (or type hint, like typing.Iterable), check if the item is an instance of that type
- If the constraint is iterable, try each value as a constraint against the item. If any validate, the constraint validates.
- If the constraint is callable, evaluate it against the item

If every pair in the schema succesfully validates against at least one pair in the item, the item validates.



