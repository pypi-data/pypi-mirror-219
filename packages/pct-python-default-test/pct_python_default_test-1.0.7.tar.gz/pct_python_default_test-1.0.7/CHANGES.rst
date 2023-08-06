Changelog
---------

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.0.7
---------
2023-07-14:
    - add codeql badge
    - move 3rd_party_stubs outside the src directory
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.0.6
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests

v1.0.5
---------
2023-xx-xx:
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

v1.0.4
---------
2023-06-26:
    - update black config
    - remove travis config
    - remove bettercodehub config
    - do not upload .egg files to pypi.org

v1.0.3
---------
2023-01-13:
    - update github actions : checkout@v3 and setup-python@v4
    - remove "better code" badges
    - remove python 3.6 tests
    - adding python 3.11 tests
    - update pypy tests to 3.9

v1.0.2
--------
2022-05-20: update github actions test matrix to python 3.10

v1.0.1
--------
2022-03-29: remedy mypy Untyped decorator makes function "cli_info" untyped

v1.0.0
---------
2022-03-25: remove listdir of ./dist, moved to lib_cicd_github

v0.1.1
---------
2020-08-01: fix pypi deploy

v0.1.0
--------
2020-07-31:
    - change1
    - change2
    - ...
