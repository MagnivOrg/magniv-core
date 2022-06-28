### Magniv tests

Goal: Create robust comprehensive unit and integration tests to empower fast development.

Structure: all tests stored in top level folder called “tests” inner folders structured by test type eg

-Tests

```
- unit_tests
- integration_tests
- standalone_tests
- utils
```

Stack:

```
pytest
	https://github.com/pytest-dev/pytest
coverage
	https://github.com/nedbat/coveragepy
```

Schematics:

```
build.py:
	Totest:
	Testing:
		requirements in nested dir
		requirements top level dir
		gets list of decorated nodes from ast
		gets all decorated tasks from file as list
		finds all files in dir that have magniv task decorators
		saves dump.json to expected path
		throws oserror if no file with decorated task is found
		throws oserror if dir specified dir not found
```
