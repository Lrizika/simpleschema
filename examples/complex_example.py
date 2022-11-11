
import simpleschema
import typing

my_schema = {
	'version': lambda v: v >= '1.9.2',
	'options-list': typing.Iterable,
	'callback': typing.Callable,
	'must-exist': typing.Any,
	'previous-message': {
		'hash': str,
	},
	'has-required-method': simpleschema.ObjectSchema({
		'requiredMethod': typing.Callable,
	}),
	'has-required-attribute': simpleschema.ObjectSchema({
		'required_attribute': typing.Any,
	}),
	('either-this', 'or-that'): ('value-a', 'value-b'),
	typing.Any: 'required-value',
}


def cb(val1, val2):
	print(val1)
	raise Exception(val2)


class ClassWithRequiredMethod:
	def requiredMethod(self):
		return str(self)


class MustBeInstantiated:
	def __init__(self):
		self.required_attribute = 'something'


valid_item = {
	'version': '2.0.1',
	'options-list': ['option-a', 'option-b'],
	'callback': cb,
	'must-exist': 2134,
	'previous-message': {
		'hash': 'asdf',
		'extraneous-key': None,
	},
	'has-required-method': ClassWithRequiredMethod,
	'has-required-attribute': MustBeInstantiated(),
	'or-that': 'value-a',
	object(): 'required-value',
}


print(
	'simpleschema.isValid(valid_item, my_schema)',
	simpleschema.validateSchema(valid_item, my_schema)
)  # True

