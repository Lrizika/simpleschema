
# simpleschema

A simple schema validator for Python

Basic usage:
```python
import simpleschema

my_schema = {
	'method': 'GET',
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
	'method': 'POST',
	'version': '0.1.9',
}

simpleschema.is_valid(item=my_item, schema=my_schema)  # True
simpleschema.is_valid(item=bad_item, schema=my_schema)  # False
```

Keys-value pairs in the schema are compared as constraints against each pair in the item, by the following methods, in order:
- Direct value comparison
- If the constraint is typing.Literal, compare its value to the value of the item
- If the constraint is a dictionary, recursively validate the item against the constraint as a schema
- If the constraint is a type (or type hint, like typing.Iterable), check if the item is an instance of that type
- If the constraint is iterable, try each value as a constraint against the item. If any validate, the constraint validates.
- If the constraint is callable, evaluate it against the item
If every pair in the schema succesfully validates against at least one pair in the item, the item validates.

