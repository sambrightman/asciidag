# -*- coding: utf-8 -*-
"""Ordering of nodes in a DAG."""

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
from collections import defaultdict


def walk_nodes(nodes):
    """Iterate over nodes in breadth-first order."""
    for node in nodes:
        yield node
    for node in nodes:
        for ancestor in walk_nodes(node.parents):
            yield ancestor


def once(nodes):
    """De-duplicate a sequence of nodes."""
    seen = {}
    for node in nodes:
        if node not in seen:
            seen[node] = True
            yield node


def sort_in_topological_order(nodes):
    """Iterate over nodes in topological order."""
    in_degree = defaultdict(lambda: 0)

    for node in nodes:
        in_degree[node] = 1

    for node in nodes:
        for parent in node.parents:
            if in_degree[parent] > 0:
                in_degree[parent] += 1

    queue = [node for node in nodes if in_degree[node] == 1]
    for node in queue:
        for parent in node.parents:
            if in_degree[parent] == 0:
                continue
            in_degree[parent] -= 1
            if in_degree[parent] == 1:
                queue.append(parent)
        in_degree[node] = 0
        yield node
