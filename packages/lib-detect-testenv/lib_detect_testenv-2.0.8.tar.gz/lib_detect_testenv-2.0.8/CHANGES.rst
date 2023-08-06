Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v2.0.8
---------
2023-07-14:
    - remove dependency click
    - remove dependency cli_exit_tools to avoid circular dependency

v2.0.7
---------
2023-07-14:
    - add codeql badge
    - move 3rd_party_stubs outside the src directory
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v2.0.6
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests

v2.0.5
---------
2023-07-11:
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

v2.0.4
---------
2023-06-26: suppress upload of .egg files to pypi.org

v2.0.3
---------
2023-01-13:
    - update github actions : checkout@v3 and setup-python@v4
    - remove "better code" badges
    - remove python 3.6 tests
    - add python 3.11 tests
    - update to pypy 3.9 tests

v2.0.2.2
---------
2022-06-02: update to github actions checkout@v3 and setup-python@v3

v2.0.2.1
--------
2022-06-01: update github actions test matrix

v2.0.2
--------
2022-03-29: remedy mypy Untyped decorator makes function "cli_info" untyped

v2.0.1
--------
2022-03-25: fix github actions windows test

v2.0.0
-------
2021-11-23:
    - add "setup.py test" detection

v1.0.2
-------
2021-11-22:
    - remove second github action yml
    - fix "setup.py test"

v1.0.1
------
2021-11-21: implement github actions

v1.0.0
------
2021-11-19: initial release
