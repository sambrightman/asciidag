def walk_nodes(nodes):
    for node in nodes:
        yield node
    for node in nodes:
        for ancestor in walk_nodes(node.parents):
            yield ancestor


def walk_nodes_once(nodes):
    seen = {}
    for node in walk_nodes(nodes):
        if node not in seen:
            seen[node] = True
            yield node
