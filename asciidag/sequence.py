# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
from collections import defaultdict


def walk_nodes(nodes):
    for node in nodes:
        yield node
    for node in nodes:
        for ancestor in walk_nodes(node.parents):
            yield ancestor


def once(nodes):
    seen = {}
    for node in nodes:
        if node not in seen:
            seen[node] = True
            yield node


def sort_in_topological_order(nodes):
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
