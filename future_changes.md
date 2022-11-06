
TODO list:
- Improve documentation
	- Correct for new return info on validateSchema
	- Add regex matching examples
	- Add reasoning for using typing.Callable
- Improve custom exceptions
	- Look into automagically appending key/value info, rather than adding it manually every time
- Improve tests
	- Test for specific item validation exceptions
	- Test for multiple failures, appropriate raised exceptions
- Add shortcut failure option
	- Terminology?
	- Fails the validation if a key matches but the value does not
- Improve testing, documentation, and examples for regex constraints
- Add DictSchema class
	- Add matching method options to ObjectSchema and DictSchema
		- Fail if no matches (default)
		- Fail if any key matches without a value match
- Add constraint and item to exceptions
	- Remove custom messages, add relevant stuff to __repr__
- Add option to abort on first failure
- Add logical operators
	- simpleschema.logical.And, .Or, .Not

Bugs to fix:
- None currently known!
	- I suspect this will change once I add tests
