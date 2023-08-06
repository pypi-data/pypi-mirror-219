========
Overview
========
.. start-badges

.. list-table::
    :stub-columns: 1

    * - code
      - |black| |mypy| |ruff|
    * - docs
      - |docs|
    * - tests
      - | |nox| |github-actions|
        | |coveralls| |codecov|
        | |codacy| |codeclimate|
    * - package
      - | |poetry| |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |black| image:: https://img.shields.io/badge/%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

.. |mypy| image:: https://www.mypy-lang.org/static/mypy_badge.svg
    :target: https://mypy-lang.org/
    :alt: Mypy

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |docs| image:: https://readthedocs.org/projects/python-no-name/badge/?style=flat
    :target: https://python-no-name.readthedocs.io/
    :alt: Documentation Status

.. |nox| image:: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
    :alt: nox
    :target: https://github.com/wntrblm/nox

.. |github-actions| image:: https://github.com/ugognw/python-no-name/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ugognw/python-no-name/actions

.. |coveralls| image:: https://coveralls.io/repos/github/ugognw/python-no-name/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://coveralls.io/github/ugognw/python-no-name?branch=main

.. |codecov| image:: https://codecov.io/gh/ugognw/python-no-name/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/ugognw/python-no-name

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/9b29574117f2476098e056d72bf1c59a
    :target: https://www.codacy.com/gh/ugognw/python-no-name
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/ugognw/python-no-name/badges/gpa.svg
   :target: https://codeclimate.com/github/ugognw/python-no-name
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/no-name.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/no-name

.. |wheel| image:: https://img.shields.io/pypi/wheel/no-name.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/no-name

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/no-name.svg
    :alt: Supported versions
    :target: https://pypi.org/project/no-name

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/no-name.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/no-name

.. |commits-since| image:: https://img.shields.io/github/commits-since/ugognw/python-no-name/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ugognw/python-no-name/compare/v0.0.0...main

.. |poetry| image:: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
    :alt: Poetry
    :target: https://python-poetry.org/

.. end-badges

An example package. Generated with `cookiecutter-pylibrary_ <https://github.com/ugognw/cookiecutter-pylibrary>`.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install no-name

You can also install the in-development version with::

    pip install https://github.com/ugognw/python-no-name/archive/main.zip


Documentation
=============

https://python-no-name.readthedocs.io/

To use the project:

.. code-block:: python

    import no_name

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
