from __future__ import print_function
import asciidag
import sys

class Node(object):
    def __init__(self, item, parents=None):
        self.item = item
        if parents is None:
            parents = []
        self.parents = parents

    def __str__(self):
        return self.item


def walk_nodes(nodes):
    for node in nodes:
        yield node
    for node in nodes:
        for ancestor in walk_nodes(node.parents):
            yield ancestor

def show_graph(graph, node):
    graph.show_commit()
    fh.write(node.item)
    if not graph.is_commit_finished():
        fh.write('\n')
        graph.show_remainder()
    fh.write('\n')

root = Node('root')
grandpa = Node('grandpa', parents=[root])
tip = Node('child', parents=[
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
])

fh = sys.stdout
graph = asciidag.Graph(fh=fh)

seen = {}
for node in walk_nodes([tip]):
    if node not in seen:
        seen[node] = True
        graph.update(node)
        show_graph(graph, node)
