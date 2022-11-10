

import typing
import re
from simpleschema import ObjectSchema


# Pairs of (schema, item)
VALID_SCHEMA_PAIRS = [
	({typing.Any: typing.Any}, {'a': 1}),
]

INVALID_SCHEMA_PAIRS = [
	({typing.Any: typing.Any}, {}),
]


# Pairs of (constraint, item)
VALID_ITEM_PAIRS = [
	# Validate due to equality
	('asdf', 'asdf'),
	(b'asdf', b'asdf'),
	(None, None),
	(1234, 1234),
	(False, False),
	((), ()),
	(True, 1),
	# Validate due to typing.Any
	(typing.Any, 'asdf'),
	(typing.Any, None),
	(typing.Any, typing.Any),
	(typing.Any, object()),
	# Validate due to regex match
	(re.compile(r'sd'), 'asdf'),
	# Validate due to typing.Literal argument equality
	(typing.Literal[21], 21),
	(typing.Literal['asdf'], 'asdf'),
	# Validate due to recursion into validateSchema
	# For further testing of validateSchema, see TestValidateSchema
	({'key': 'value'}, {'key': 'value', 'extra_key': None}),
	# Validate due to type checking
	(str, 'asdf'),
	(int, 1234),
	(object, object()),
	(tuple, ()),
	(type(None), None),
	(callable, lambda _: True),
	(type, str),
	(typing.Iterable, []),
	# Validate due to truthy callable
	(bool.__call__, 1),
	(lambda v: v, True),
	(lambda v: v > 50, 60),
	(lambda v: not v, False),
	(lambda v: v > '1.0.1', '2.0.0'),
]

