Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.1.7
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py

v1.1.6
--------
2022-03-25: implement github actions

v1.1.5
--------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

v1.1.4
--------
2020-08-08: service release
    - fix documentation
    - fix travis
    - deprecate pycodestyle
    - implement flake8

v1.1.3
---------
2020-08-01: fix pypi deploy

v1.1.2
--------
2020-07-31: fix travis build

0.1.1
--------
2020-07-29: feature release
    - use the new pizzacutter template
    - use cli_exit_tools

0.1.0
--------
2020-07-16: feature release
    - fix cli test
    - enable traceback option on cli errors
    - manage project with PizzaCutter

0.0.1
--------
2019-09-03: Initial public release
