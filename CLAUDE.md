# Project Instructions

## Python Environment

- All python commands and scripts (like pytest) must be run with a prefix "uv run ..." to set up the virtual environment correctly

## Testing

- Use pytest to run tests (uv run pytest...), do not use django tests (./manage.py test)
- When creating new tests, prefer pytest style tests
- When creating tests, ensure that the name of the test includes the module name, so as not to confuse pytest with naming collisions
  - Example: `test_module_topic.py` not `test_topic.py` (which could apply to any module)

## Code Standards

- When creating new scripts of any type, ensure that the file has a terminating newline at the end of the script
  - Exception: empty files such as an empty `__init__.py`

## Bug Handling

- If bugs or misbehaviours are discovered, don't make tests allow for it, instead attempt to fix the issue and notify of its existence.
