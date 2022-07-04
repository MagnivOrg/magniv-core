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
    integration_tests:
        todo:
	    - test where there are nested folders with tasks in them, make sure that all those tasks show in the `dump.json` and that the `dump.json` is accurate
	    - test when there are multiple task files in the same folder and make sure all of them show up
	    - test when there is a nested folder that has its own `requirements.txt` -- verify that the `dump.json` reflects that the correct `requirements.txt` is being used
	    - test when there is a nested folder w/o a `requirements.txt`, make sure it uses the next parents `requirements.txt`
	- test_name
    unit_tests:
        todo:
        test_build.py:
            - requirements in nested dir
            - requirements top level dir
            - gets list of decorated nodes from ast
            - gets all decorated tasks from file as list
            - finds all files in dir that have magniv task decorators
            - saves dump.json to expected path
            - throws oserror if no file with decorated task is found
            - throws oserror if dir specified dir not found
	    - multiple tasks within one file 
```
