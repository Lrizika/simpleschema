
import unittest
from simpleschema.validate import validateItem, validateSchema
import typing
import logging
import sys


class TestValidateSchema(unittest.TestCase):
	pass


class TestValidateItem(unittest.TestCase):
	def test_validates_success(self):
		# Pairs of (schema constraint, item)
		valid_schema_pairs = [
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
			# Validate due to typing.Literal argument equality
			(typing.Literal[21], 21),
			(typing.Literal['asdf'], 'asdf'),
		]

		for pair in valid_schema_pairs:
			try:
				self.assertTrue(
					validateItem(schema_val=pair[0], item_val=pair[1]),
				)
			except Exception:
				print(f'Failed with schema constraint {pair[0]}, item {pair[1]}')
				raise

	def test_validates_failure(self):
		invalid_schema_pairs = [
			(object(), object()),  # Noteably not the same object
			(1234, 1),
			(None, 0),
			((), 0),
			('asdf', 'a'),
			(b'asdf', 'a'),
		]

		for pair in invalid_schema_pairs:
			with self.assertRaises(ValueError, msg=f'Failed with schema constraint {pair[0]}, item {pair[1]}'):
				validateItem(schema_val=pair[0], item_val=pair[1])


if __name__ == '__main__':
	if ('-vv' in sys.argv) or ('--very-verbose' in sys.argv):
		logging.basicConfig(level=logging.DEBUG, format='    %(funcName)s %(message)s')
	unittest.main()
