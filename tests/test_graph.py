# -*- coding: utf-8 -*-
"""Tests the graph module."""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest


def verify_output(capture, expected):
    """Verify captured standard output matches the expected string."""
    captured = capture.readouterr()
    assert captured.out == expected


def test_linear(graph, simple_nodes, capfd):
    """Test the simple set of nodes."""
    graph.show_nodes(simple_nodes)
    verify_output(capfd, r"""* Second
* sixth
* fifth
* fourth
* third
* second
* initial
""")


@pytest.mark.xfail
def test_branched(graph, branched_nodes, capfd):
    """Test the branched set of nodes."""
    graph.show_nodes(branched_nodes)
    verify_output(capfd, r"""*   Merge branch 'side'
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
def test_tangled(graph, tangled_nodes, capfd):
    """Test the complex set of nodes."""
    graph.show_nodes(tangled_nodes)
    verify_output(capfd, r"""*   Merge tag 'reach'
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
