# -*- coding: utf-8 -*-
"""Tests the graph module."""

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
# pylint: disable=redefined-outer-name

import pytest

from asciidag.graph import Graph
from asciidag.node import Node


# FIXME: fails to capture stdout
@pytest.fixture
def graph():
    """Fixture to supply an empty graph."""
    return Graph(use_color=False)


@pytest.fixture
def simple_nodes():
    """Fixture to supply a simple, linear set of nodes."""
    return [Node.from_list(
        "Second",
        "sixth",
        "fifth",
        "fourth",
        "third",
        "second",
        "initial",
    )]


@pytest.fixture
def branched_nodes():
    """Fixture to supply a simple set of nodes with one feature branch."""
    third = Node.from_list("third", "second", "initial")
    tip = Node("Merge branch 'side'", parents=[
        Node("Second", parents=[
            Node("sixth", parents=[
                Node("fifth", parents=[
                    Node("fourth", parents=[third]),
                ]),
            ]),
        ]),
        Node("side-2", parents=[
            Node("side-1", parents=[third]),
        ]),
    ])
    return [tip]


@pytest.fixture
def tangled_nodes():
    """Fixture to supply a complicated set of nodes with multiple branches."""
    second = Node.from_list("second", "initial")
    third = Node("third", parents=[second])
    fifth = Node("fifth", parents=[
        Node("fourth", parents=[third]),
    ])
    side1 = Node("side-1", parents=[third])
    tangle = Node("Merge tag 'tangle'", parents=[
        Node("Merge branch 'side' (early part) into tangle", parents=[
            Node("Merge branch 'master' (early part) into tangle", parents=[
                Node("tangle-a", parents=[second]),
                fifth,
            ]),
            side1,
        ]),
        Node("Merge branch 'side'", parents=[
            Node("side-2", parents=[side1]),
            Node("Second", parents=[
                Node("sixth", parents=[fifth]),
            ])
        ]),
    ])
    tip = Node("Merge tag 'reach'", parents=[
        Node("Merge tags 'octopus-a' and 'octopus-b'", parents=[
            Node("seventh", parents=[tangle]),
            Node("octopus-b", parents=[tangle]),
            Node("octopus-a", parents=[tangle]),
        ]),
        Node("reach", parents=[tangle]),
    ])
    return [tip]


def verify_out(capfd, expected):
    """Verify captured standard output/error matches the expected string, whilst also displaying it."""
    out, _ = capfd.readouterr()
    print(out)
    assert expected == out


def test_linear(simple_nodes, capfd):
    """Test the simple set of nodes."""
    graph = Graph(use_color=False)
    graph.show_nodes(simple_nodes)
    verify_out(capfd, r"""* Second
* sixth
* fifth
* fourth
* third
* second
* initial
""")


@pytest.mark.xfail
def test_branched(branched_nodes, capfd):
    """Test the branched set of nodes."""
    graph = Graph(use_color=False)
    graph.show_nodes(branched_nodes)
    verify_out(capfd, r"""*   Merge branch 'side'
|\
| * side-2
| * side-1
* | Second
* | sixth
* | fifth
* | fourth
|/
* third
* second
* initial""")


@pytest.mark.xfail
def test_tangled(tangled_nodes, capfd):
    """Test the complex set of nodes."""
    graph = Graph(use_color=False)
    graph.show_nodes(tangled_nodes)
    verify_out(capfd, r"""*   Merge tag 'reach'
|\
| \
|  \
*-. \   Merge tags 'octopus-a' and 'octopus-b'
|\ \ \
* | | | seventh
| | * | octopus-b
| |/ /
|/| |
| * | octopus-a
|/ /
| * reach
|/
*   Merge branch 'tangle'
|\
| *   Merge branch 'side' (early part) into tangle
| |\
| * \   Merge branch 'master' (early part) into tangle
| |\ \
| * | | tangle-a
* | | |   Merge branch 'side'
|\ \ \ \
| * | | | side-2
| | |_|/
| |/| |
| * | | side-1
* | | | Second
* | | | sixth
| |_|/
|/| |
* | | fifth
* | | fourth
|/ /
* | third
|/
* second
* initial""")
