
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

print(
	'simpleschema.isValid(item=my_item, schema=my_schema)',
	simpleschema.isValid(item=my_item, schema=my_schema)
)  # True
print(
	'simpleschema.isValid(item=bad_item, schema=my_schema)',
	simpleschema.isValid(item=bad_item, schema=my_schema)
)  # False

