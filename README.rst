asciidag - draw DAGs as ASCII art
=================================

|build-status| |coverage|

.. |build-status| image:: https://travis-ci.org/sambrightman/asciidag.svg?branch=master
    :target: https://travis-ci.org/sambrightman/asciidag
    :alt: Travis CI status

.. |coverage| image:: https://coveralls.io/repos/github/sambrightman/asciidag/badge.svg?branch=master
    :target: https://coveralls.io/github/sambrightman/asciidag?branch=master
    :alt: Coverage

Overview
--------

This is a direct port of the `Git`_ log graphing code, which draws
directed acyclic commit graphs as ASCII art. It was done very
mechnically and quickly, so the code is not Pythonic. Dependencies on
`Git`_ specifics should be gone but and look and feel remains.

This project is alpha quality and subject to breaking API changes.

If you are thinking about doing a large refactoring, please submit an
issue for discussion first; I consider it potentially worth staying
close to the `Git`_ source.


Usage
-----

.. code-block:: bash

    git clone https://github.com/sambrightman/asciidag.git
    cd asciidag && pip install .
    tests/demo.py

You likely need to use ``sudo`` for the install unless you work in a
`Python virtual environment`_ or use the ``--user`` option to
``pip``. Will soon be on `PyPI`_.

.. image:: images/demo.png?raw=true
   :alt: Demonstration screenshot

:copyright: © 2016 Sam Brightman
:license: Mozilla Public License version 2.0, see LICENSE for more details.

.. _Python virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs
.. _Git: https://git-scm.com
.. _PyPI: https://pypi.python.org
