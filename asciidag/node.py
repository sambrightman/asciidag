class Node(object):
    def __init__(self, item, parents=None):
        self.item = item
        if parents is None:
            parents = []
        self.parents = parents

    def __str__(self):
        return str(self.item)

    @staticmethod
    def from_dict(d):
        return [Node(k, Node.from_dict(v)) for k, v in d.items()]
