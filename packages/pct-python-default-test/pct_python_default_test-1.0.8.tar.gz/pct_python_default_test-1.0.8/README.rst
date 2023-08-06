pct_python_default_test
=======================


Version v1.0.8 as of 2023-07-14 see `Changelog`_

|build_badge| |codeql| |license| |jupyter|
|black| |codecov| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/pct_python_default_test/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/pct_python_default_test/actions/workflows/python-package.yml


.. |codeql| image:: https://github.com/bitranox/pct_python_default_test/actions/workflows/codeql-analysis.yml/badge.svg?event=push
   :target: https://github.com//bitranox/pct_python_default_test/actions/workflows/codeql-analysis.yml

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/pct_python_default_test/master?filepath=pct_python_default_test.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/pct-python-default-test?label=PyPI%20Package
   :target: https://badge.fury.io/py/pct_python_default_test

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/pct_python_default_test
   :target: https://codecov.io/gh/bitranox/pct_python_default_test

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/pct_python_default_test?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/pct_python_default_test/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/pct_python_default_test?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/pct_python_default_test/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/pct_python_default_test?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/pct_python_default_test/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://snyk.io/test/github/bitranox/pct_python_default_test/badge.svg
   :target: https://snyk.io/test/github/bitranox/pct_python_default_test

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/pct-python-default-test
   :target: https://pypi.org/project/pct-python-default-test/
   :alt: PyPI - Downloads

This is the test project created using PizzaCutter

PizzaCutter is a command-line utility that creates and updates software projects in any language from PizzaCutter project templates.

The purpose of this repository is, to show and test a newly created project from the python default template.


More Information can be found here :
    - `PizzaCutter <https://github.com/bitranox/PizzaCutter>`_
    - `PizzaCutter python default template <https://github.com/bitranox/pct_python_default>`_
    - more templates to come

----

automated tests, Github Actions, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.8.0 or newer

tested on recent linux with python 3.8, 3.9, 3.10, 3.11, 3.12-dev, pypy-3.9, pypy-3.10 - architectures: amd64

`100% code coverage <https://codeclimate.com/github/bitranox/pct_python_default_test/test_coverage>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS, Windows <https://github.com/bitranox/pct_python_default_test/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/pct_python_default_test/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/pct_python_default_test/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/pct_python_default_test/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=pct_python_default_test.ipynb>`_

Usage
-----------

- example for including docstrings

.. code-block:: python

    def main() -> None:
        """
        the main method, prints hello world


        Parameter
        ----------
        none
            none


        Result
        ----------
        none


        Exceptions
        ----------
        none


        Examples
        ----------

        >>> main()
        Hello World - by PizzaCutter

        """

Usage from Commandline
------------------------

.. code-block::

   Usage: pct_python_default_test [OPTIONS] COMMAND [ARGS]...

     a pizzacutter default test project, crated with PizzaCutter and the
     PizzaCutter default python template

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program informations

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools




- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/pct_python_default_test.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest development version :
    pct_python_default_test @ git+https://github.com/bitranox/pct_python_default_test.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version, including test dependencies from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/pct_python_default_test.git
    $ cd pct_python_default_test
    python -m pip install -e .[test]

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/pct_python_default_test.git
    $ cd pct_python_default_test

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    cli_exit_tools

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/pct_python_default_test/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
---------

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.0.8
---------
2023-07-14:
    - move 3rd_party_stubs directory to ``./.3rd_party_stubs``

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

