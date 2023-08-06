Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.1.15
---------
2023-07-14:
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.1.14
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests

v1.1.13
---------
2023-07-13:
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

v1.1.12.2
---------
2022-06-01: update to github actions checkout@v3 and setup-python@v3

v1.1.12.1
---------
2022-06-01: update github actions test matrix

v1.1.12
--------
2022-03-29: remedy mypy Untyped decorator makes function "cli_info" untyped

v1.1.11
--------
2022-03-25: fix github actions windows test

v1.1.10
-------
2021-11-22
    - fix "setup.py test"

v1.1.9
------
2021-11-21: service release
    - implement github actions
    - implement check for test environment on __init__

v1.1.8
--------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

v1.1.7
---------
2020-08-08: service release
    - fix documentation
    - fix travis
    - deprecate pycodestyle
    - implement flake8

v1.1.6
---------
2020-08-07: fix wheels

v1.1.5
---------
2020-08-01: fix pypi deploy

v1.1.4
-------
2020-07-31: initial PyPi release
