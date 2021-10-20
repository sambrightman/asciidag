asciidag - draw DAGs as ASCII art
=================================

|build-status| |win-build-status| |coveralls-coverage| |codecov-coverage| |pypi-version| |pypi-wheel|

.. |build-status| image:: https://travis-ci.org/sambrightman/asciidag.svg?branch=master
    :target: https://travis-ci.org/sambrightman/asciidag
    :alt: Travis CI status

.. |win-build-status| image:: https://ci.appveyor.com/api/projects/status/t4dv71xsfcifk8mg/branch/master?svg=true
    :target: https://ci.appveyor.com/project/sambrightman/asciidag
    :alt: AppVeyor CI status

.. |coveralls-coverage| image:: https://coveralls.io/repos/github/sambrightman/asciidag/badge.svg?branch=master
    :target: https://coveralls.io/github/sambrightman/asciidag?branch=master
    :alt: Coveralls coverage

.. |codecov-coverage| image:: https://codecov.io/gh/sambrightman/asciidag/branch/master/graph/badge.svg?token=tHv0ZDOJKA
    :target: https://codecov.io/gh/sambrightman/asciidag
    :alt: Codecov coverage

.. |pypi-version| image:: https://img.shields.io/pypi/v/asciidag
    :target: https://pypi.org/project/asciidag/
    :alt: PyPI version

.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/asciidag
    :alt: PyPI wheel

Overview
--------

This is a direct port of the `Git`_ log graphing code, which draws
directed acyclic commit graphs as ASCII art. It was done very
mechanically and quickly, so the code is not Pythonic. Dependencies on
`Git`_ specifics should be gone but look and feel remains.

This project is alpha quality and subject to breaking API changes.

    .. note::
       💡
       If you are thinking about doing a large refactoring, please submit
       an issue for discussion first; I consider it potentially worthwhile
       to stay close to the `Git`_ source.

Installation
------------

Available for install/upgrade from `PyPI`_:

.. code-block:: bash

    pip install -U asciidag

As usual, it is best to install your packages into a `virtual environment`_.

Usage
-----

``examples/demo.py`` is included in the installation directory and is
executable. The core functionality is:

.. code:: python
   
       from asciidag.graph import Graph
       from asciidag.node import Node
   
       graph = Graph()
   
       root = Node('root')
       grandpa = Node('grandpa', parents=[root])
       tips = [
           Node('child', parents=[
               Node('mom', parents=[
                   Node('grandma', parents=[
                       Node('greatgrandma', parents=[]),
                   ]),
                   grandpa,
               ]),
               Node('dad', parents=[
                   Node('bill', parents=[
                       Node('martin'),
                       Node('james'),
                       Node('paul'),
                       Node('jon'),
                   ])]),
               Node('stepdad', parents=[grandpa]),
           ]),
           Node('foo', [Node('bar')]),
       ]
   
       graph.show_nodes(tips)

Output:

.. image:: images/demo.png?raw=true
   :alt: Demonstration screenshot

:copyright: © 2016 Sam Brightman
:license: GNU General Public License v2.0, see LICENSE for more details.

.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs
.. _Git: https://git-scm.com
.. _PyPI: https://pypi.python.org
