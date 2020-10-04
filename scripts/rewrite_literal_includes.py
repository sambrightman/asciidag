#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rewrite literal include directives to be compatible with hosts that ban them."""

from __future__ import absolute_import, division, print_function, unicode_literals

import re
import sys
from io import open

import docutils.nodes
import docutils.frontend
import docutils.parsers.rst
import docutils.utils

# this is all fairly crazy but interesting to write


def rewrite_literal_includes(input_filename="README.rst.in", output_filename="README.rst"):
    """Rewrite literal include directives from a reStructuredText file to their resulting blocks."""
    if output_filename is None:
        output_filename = input_filename
    rewritten_text = _unparse_literal_includes(input_filename)
    with open(output_filename, mode="w", encoding="utf-8") as output_fh:
        output_fh.write(rewritten_text)


def _unparse_literal_includes(filename):
    rst_document, text = _parse_rst(filename)
    source_map = {node.attributes["source"]: lambda indent, node=node: _unparse_node(node, indent)
                  for node in rst_document.traverse(docutils.nodes.literal_block) if "source" in node.attributes}
    return re.sub(r"(?P<prefix>\n*)^(?P<indent>[\t ]*)\.\. include:: (?P<source>\S+).*?(?P<suffix>\n\s*)$",
                  lambda match: "{}{}{}".format(match.group("prefix"),
                                                source_map[match.group("source")](match.group("indent")),
                                                match.group("suffix")),
                  text,
                  flags=re.MULTILINE | re.DOTALL)


def _parse_rst(filename):
    with open(filename, encoding="utf-8") as document_fh:
        parser = docutils.parsers.rst.Parser()
        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(components=components).get_default_values()
        document = docutils.utils.new_document(filename, settings=settings)
        text = document_fh.read()
        parser.parse(text, document)
        return document, text


def _unparse_node(node, indent):
    classes = iter(node.attributes["classes"])
    names = iter(node.attributes["names"])
    primary_class = next(classes, None)
    if primary_class == "code":
        language = next(classes, "")
        # warn if any remain?
        primary_class = next(classes, None)
        primary_name = next(names, None)
        lines = [".. code:: {}".format(language)]
    else:
        # warn if any remain?
        primary_name = next(names, None)
        lines = [".. parsed-literal::"]

    if primary_class is not None:
        lines.append(":class: {}".format(primary_class))
    if primary_name is not None:
        lines.append(":name: {}".format(primary_name))
    lines.append("")
    lines.extend(node.astext().splitlines())

    return "\n   ".join("{}{}".format(indent, line) for line in lines)


if __name__ == "__main__":
    rewrite_literal_includes(*sys.argv[1:])  # pylint: disable=no-value-for-parameter
