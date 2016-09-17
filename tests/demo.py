#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function

from asciidag.graph import Graph
from asciidag.node import Node
from asciidag.sequence import walk_nodes_once


if __name__ == '__main__':
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

    graph.show_nodes(walk_nodes_once(tips))
