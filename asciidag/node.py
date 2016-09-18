class InvalidNodeException(Exception):
    pass


class Node(object):
    def __init__(self, item, parents=None):
        self.item = item
        if parents is None:
            parents = []
        try:
            iter(parents)
        except TypeError:
            raise InvalidNodeException(str(item))
        self.parents = parents

    def __str__(self):
        return str(self.item)

    @staticmethod
    def from_dict(d):
        return [Node(k, Node.from_dict(v)) for k, v in d.items()]

    @staticmethod
    def from_list(head, *tail):
        if not tail:
            return Node(head, [])
        return Node(head, [Node.from_list(*tail)])
