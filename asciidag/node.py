# -*- coding: utf-8 -*-
"""Individual items within a DAG."""

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function


class InvalidNodeException(Exception):
    """Indicates an invalid attempt to create a node."""


class Node(object):  # pylint: disable=useless-object-inheritance
    """A node in a DAG with zero or more parents."""

    def __init__(self, item, parents=None):
        """Construct a node with given parents.

        Args:
            item (:obj:) item contained in the node.
            parents (:obj:`list` of :obj:) parents of the item, if any.
        """
        self.item = item
        if parents is None:
            parents = []
        try:
            iter(parents)
        except TypeError:
            raise InvalidNodeException(str(item))  # pylint: disable=raise-missing-from
        self.parents = parents

    def __str__(self):
        """Return the string representation of the item in the node."""
        return str(self.item)

    @staticmethod
    def from_dict(dct):
        """Construct a nested list of nodes from a nested dict.

        Each key is the item of a node in the list. Each value is
        expected to be a (nested) dictionary of parents of that item,
        with empty dictionaries acting as terminators.

        Args:
            dct (:obj:`dict`) nested dictionary of item to parent mappings.

        """
        return [Node(k, Node.from_dict(v)) for k, v in dct.items()]

    @staticmethod
    def from_list(head, *tail):
        """Construct a node with given parents.

        Args:
            head (:obj:) item contained in the node.
            tail (:obj:`list` of :obj:) parents of the item.
        """
        if not tail:
            return Node(head, [])
        return Node(head, [Node.from_list(*tail)])  # pylint: disable=no-value-for-parameter
