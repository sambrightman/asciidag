# -*- coding: utf-8 -*-
"""Tests the graph module."""

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function

import pytest

from asciidag.graph import Graph


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
