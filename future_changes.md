
TODO list:
- Improve documentation
	- Top Priority!
- Add logging
	- Consider loglevels
		- Debug should tell all match/mismatch results
		- Info should probably only tell matches?
- Add custom exceptions
	- Look into automagically appending key/value info, rather than adding it manually every time

Bugs to fix:
- Infinite recursion error:
```python
>>> i3
{('c', 'a'): {'b': 1}, 3: 2}
>>> s3
{'a': {'b': 1}, <class 'object'>: 2}
>>> validate.validateSchema(i3, s3)
```
