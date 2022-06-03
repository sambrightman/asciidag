# -*- coding: utf-8 -*-
"""ASCII representation of directed acyclic graphs (DAGs).

This is almost a straight port of Git's graph.c.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from enum import Enum

from .color import COLUMN_COLORS_ANSI
from .sequence import walk_nodes, once, sort_in_topological_order

__all__ = ('Graph',)


class Column(object):  # pylint: disable=bad-option-value,useless-object-inheritance
    """A single column of output.

    Attributes:
        commit -- The parent commit of this column.
        color  -- The color to (optionally) print this column in.
                  This is an index into column_colors.

    """

    def __init__(self, commit, color):
        self.commit = commit
        self.color = color


class GraphState(Enum):
    """The current state of the state machine."""

    PADDING = 0
    SKIP = 1
    PRE_COMMIT = 2
    COMMIT = 3
    POST_MERGE = 4
    COLLAPSING = 5


# The commit currently being processed
#         struct commit *commit
#
# The number of interesting parents that this commit has.
# Note that this is not the same as the actual number of parents.
# This count excludes parents that won't be printed in the graph
# output, as determined by is_interesting().
#         int num_parents
#
# The width of the graph output for this commit.
# All rows for this commit are padded to this width, so that
# messages printed after the graph output are aligned.
#         int width
#
# The next expansion row to print
# when state is GraphState.PRE_COMMIT
#         int expansion_row
#
# The current output state.
# This tells us what kind of line next_line() should output.
#         enum graph_state state
#
# The output state for the previous line of output.
# This is primarily used to determine how the first merge line
# should appear, based on the last line of the previous commit.
#         enum graph_state prev_state
#
# The index of the column that refers to this commit.
# If none of the incoming columns refer to this commit,
# this will be equal to num_columns.
#         int commit_index
#
# The commit_index for the previously displayed commit.
# This is used to determine how the first line of a merge
# graph output should appear, based on the last line of the
# previous commit.
#         int prev_commit_index
#
# The maximum number of columns that can be stored in the columns
# and new_columns arrays. This is also half the number of entries
# that can be stored in the mapping and new_mapping arrays.
#         int column_capacity
#
# The number of columns (also called "branch lines" in some places)
#         int num_columns
#
# The number of columns in the new_columns array
#         int num_new_columns
#
# The number of entries in the mapping array
#         int mapping_size
#
# The column state before we output the current commit.
#         struct column *columns
#
# The new column state after we output the current commit.
# Only valid when state is GraphState.COLLAPSING.
#         struct column *new_columns
#
# An array that tracks the current state of each
# character in the output line during state GraphState.COLLAPSING.
# Each entry is -1 if this character is empty, or a non-negative
# integer if the character contains a branch line. The value of
# the integer indicates the target position for this branch line.
# (I.e., this array maps the current column positions to their
# desired positions.)
#
# The maximum capacity of this array is always
# sizeof(int) * 2 * column_capacity.
#         int *mapping
#
# A temporary array for computing the next mapping state
# while we are outputting a mapping line. This is stored as part
# of the git_graph simply so we don't have to allocate a new
# temporary array each time we have to output a collapsing line.
#         int *new_mapping
#
# The current default column color being used. This is
# stored as an index into the array column_colors.
#         unsigned short default_column_color
class Graph(object):  # pylint: disable=too-many-instance-attributes,bad-option-value,useless-object-inheritance
    """A state machine for processing DAG nodes into ASCII graphs."""

    def __init__(self,
                 fh=None,
                 first_parent_only=False,
                 use_color=True,
                 column_colors=None):
        """Create a state machine for parsing and displaying graph nodes.

        Args:
            fh (:obj:`file`): file handle to write the ASCII representation to.
            first_parent_only (:obj:`bool): display graph as if each node only had its first parent.
            use_color (:obj:`bool`): whether to use colored output.
            column_colors (:obj:`list` of :obj:`str`): list of ANSI control sequences to use for each lineage "column".
        """
        self.commit = None
        self.buf = ''

        if fh is None:
            self.outfile = sys.stdout
        else:
            self.outfile = fh
        self.first_parent_only = first_parent_only
        self.use_color = use_color
        if column_colors is None:
            self.column_colors = COLUMN_COLORS_ANSI
        else:
            self.column_colors = column_colors

        self.num_parents = 0
        self.width = 0
        self.expansion_row = 0
        self.state = GraphState.PADDING
        self.prev_state = GraphState.PADDING
        self.commit_index = 0
        self.prev_commit_index = 0
        self.num_columns = 0
        self.num_new_columns = 0
        self.mapping_size = 0
        # Start the column color at the maximum value, since we'll
        # always increment it for the first commit we output.
        # This way we start at 0 for the first commit.
        self.default_column_color = len(self.column_colors) - 1

        self.columns = {}
        self.new_columns = {}
        self.mapping = {}
        self.new_mapping = {}

    def show_nodes(self, tips):
        """Show an ASCII DAG for the nodes provided.

        Nodes are walked and returned without duplicates and then
        sorted topologically (a requirement of the algorithm). The
        original Git API is then used internally to display the graph
        line-by-line, outputting the Node's content at the relevant
        point.

        Args:
            tips (:obj:`list` of :obj:`Node`): tips of trees to display

        """
        nodes = sort_in_topological_order(list(once(walk_nodes(tips))))
        for node in nodes:
            self._update(node)
            self._show_commit()
            self.outfile.write(node.item)
            if not self._is_commit_finished():
                self.outfile.write('\n')
                self._show_remainder()
            self.outfile.write('\n')

    def _write_column(self, col, col_char):
        if col.color is not None:
            self.buf += self.column_colors[col.color]
        self.buf += col_char
        if col.color is not None:
            self.buf += self.column_colors[-1]

    def _update_state(self, state):
        self.prev_state = self.state
        self.state = state

    def _interesting_parents(self):
        for parent in self.commit.parents:
            yield parent
            if self.first_parent_only:
                break

    def _get_current_column_color(self):
        if not self.use_color:
            return None
        return self.default_column_color

    def _increment_column_color(self):
        self.default_column_color = ((self.default_column_color + 1)
                                     % len(self.column_colors))

    def _find_commit_color(self, commit):
        for i in range(self.num_columns):
            if self.columns[i].commit == commit:
                return self.columns[i].color
        return self._get_current_column_color()

    def _insert_into_new_columns(self, commit, mapping_index):
        # If the commit is already in the new_columns list, we don't need to
        # add it. Just update the mapping correctly.
        for i in range(self.num_new_columns):
            if self.new_columns[i].commit == commit:
                self.mapping[mapping_index] = i
                return mapping_index + 2

        # This commit isn't already in new_columns. Add it.
        column = Column(commit, self._find_commit_color(commit))
        self.new_columns[self.num_new_columns] = column
        self.mapping[mapping_index] = self.num_new_columns
        self.num_new_columns += 1
        return mapping_index + 2

    def _update_width(self, is_commit_in_existing_columns):
        # Compute the width needed to display the graph for this commit.
        # This is the maximum width needed for any row. All other rows
        # will be padded to this width.
        #
        # Compute the number of columns in the widest row:
        # Count each existing column (self.num_columns), and each new
        # column added by this commit.
        max_cols = self.num_columns + self.num_parents

        # Even if the current commit has no parents to be printed, it
        # still takes up a column for itself.
        if self.num_parents < 1:
            max_cols += 1

        # We added a column for the current commit as part of
        # self.num_parents. If the current commit was already in
        # self.columns, then we have double counted it.
        if is_commit_in_existing_columns:
            max_cols -= 1

        # Each column takes up 2 spaces
        self.width = max_cols * 2

    def _update_columns(self):
        # Swap self.columns with self.new_columns
        # self.columns contains the state for the previous commit,
        # and new_columns now contains the state for our commit.
        #
        # We'll re-use the old columns array as storage to compute the new
        # columns list for the commit after this one.
        self.columns, self.new_columns = self.new_columns, self.columns
        self.num_columns = self.num_new_columns
        self.num_new_columns = 0

        # Now update new_columns and mapping with the information for the
        # commit after this one.
        #
        # First, make sure we have enough room. At most, there will
        # be self.num_columns + self.num_parents columns for the next
        # commit.
        max_new_columns = self.num_columns + self.num_parents

        # Clear out self.mapping
        self.mapping_size = 2 * max_new_columns
        for i in range(self.mapping_size):
            self.mapping[i] = -1

        # Populate self.new_columns and self.mapping
        #
        # Some of the parents of this commit may already be in
        # self.columns. If so, self.new_columns should only contain a
        # single entry for each such commit. self.mapping should
        # contain information about where each current branch line is
        # supposed to end up after the collapsing is performed.
        seen_this = False
        mapping_idx = 0
        is_commit_in_columns = True
        for i in range(self.num_columns + 1):
            if i == self.num_columns:
                if seen_this:
                    break
                is_commit_in_columns = False
                col_commit = self.commit
            else:
                col_commit = self.columns[i].commit

            if col_commit == self.commit:
                old_mapping_idx = mapping_idx
                seen_this = True
                self.commit_index = i
                for parent in self._interesting_parents():
                    # If this is a merge, or the start of a new
                    # childless column, increment the current
                    # color.
                    if self.num_parents > 1 or not is_commit_in_columns:
                        self._increment_column_color()
                    mapping_idx = self._insert_into_new_columns(
                        parent,
                        mapping_idx)
                # We always need to increment mapping_idx by at
                # least 2, even if it has no interesting parents.
                # The current commit always takes up at least 2
                # spaces.
                if mapping_idx == old_mapping_idx:
                    mapping_idx += 2
            else:
                mapping_idx = self._insert_into_new_columns(col_commit,
                                                            mapping_idx)

        # Shrink mapping_size to be the minimum necessary
        while (self.mapping_size > 1
               and self.mapping[self.mapping_size - 1] < 0):
            self.mapping_size -= 1

        # Compute self.width for this commit
        self._update_width(is_commit_in_columns)

    def _update(self, commit):
        self.commit = commit
        self.num_parents = len(list(self._interesting_parents()))

        # Store the old commit_index in prev_commit_index.
        # update_columns() will update self.commit_index for this
        # commit.
        self.prev_commit_index = self.commit_index

        # Call update_columns() to update
        # columns, new_columns, and mapping.
        self._update_columns()
        self.expansion_row = 0

        # Update self.state.
        # Note that we don't call update_state() here, since
        # we don't want to update self.prev_state. No line for
        # self.state was ever printed.
        #
        # If the previous commit didn't get to the GraphState.PADDING state,
        # it never finished its output. Goto GraphState.SKIP, to print out
        # a line to indicate that portion of the graph is missing.
        #
        # If there are 3 or more parents, we may need to print extra rows
        # before the commit, to expand the branch lines around it and make
        # room for it. We need to do this only if there is a branch row
        # (or more) to the right of this commit.
        #
        # If there are less than 3 parents, we can immediately print the
        # commit line.
        if self.state != GraphState.PADDING:
            self.state = GraphState.SKIP
        elif (self.num_parents >= 3
              and self.commit_index < (self.num_columns - 1)):
            self.state = GraphState.PRE_COMMIT
        else:
            self.state = GraphState.COMMIT

    def _is_mapping_correct(self):
        # The mapping is up to date if each entry is at its target,
        # or is 1 greater than its target.
        # (If it is 1 greater than the target, '/' will be printed, so it
        # will look correct on the next row.)
        for i in range(self.mapping_size):
            target = self.mapping[i]
            if target < 0:
                continue
            if target == i // 2:
                continue
            return False
        return True

    def _pad_horizontally(self, chars_written):
        # Add additional spaces to the end of the string, so that all
        # lines for a particular commit have the same width.
        #
        # This way, fields printed to the right of the graph will remain
        # aligned for the entire commit.
        if chars_written >= self.width:
            return

        extra = self.width - chars_written
        self.buf += ' ' * extra

    def _output_padding_line(self):
        # Output a padding row, that leaves all branch lines unchanged
        for i in range(self.num_new_columns):
            self._write_column(self.new_columns[i], '|')
            self.buf += ' '

        self._pad_horizontally(self.num_new_columns * 2)

    def _output_skip_line(self):
        # Output an ellipsis to indicate that a portion
        # of the graph is missing.
        self.buf += '...'
        self._pad_horizontally(3)

        if self.num_parents >= 3 and self.commit_index < self.num_columns - 1:
            self._update_state(GraphState.PRE_COMMIT)
        else:
            self._update_state(GraphState.COMMIT)

    def _output_pre_commit_line(self):
        # This function formats a row that increases the space around a commit
        # with multiple parents, to make room for it. It should only be
        # called when there are 3 or more parents.
        #
        # We need 2 extra rows for every parent over 2.
        assert self.num_parents >= 3, 'not enough parents to add expansion row'
        num_expansion_rows = (self.num_parents - 2) * 2

        # self.expansion_row tracks the current expansion row we are on.
        # It should be in the range [0, num_expansion_rows - 1]
        assert (0 <= self.expansion_row < num_expansion_rows), \
            'wrong number of expansion rows'

        # Output the row
        seen_this = False
        chars_written = 0
        for i in range(self.num_columns):
            col = self.columns[i]
            if col.commit == self.commit:
                seen_this = True
                self._write_column(col, '|')
                self.buf += ' ' * self.expansion_row
                chars_written += 1 + self.expansion_row
            elif seen_this and (self.expansion_row == 0):
                # This is the first line of the pre-commit output.
                # If the previous commit was a merge commit and
                # ended in the GraphState.POST_MERGE state, all branch
                # lines after self.prev_commit_index were
                # printed as "\" on the previous line. Continue
                # to print them as "\" on this line. Otherwise,
                # print the branch lines as "|".
                if (self.prev_state == GraphState.POST_MERGE
                        and self.prev_commit_index < i):
                    self._write_column(col, '\\')
                else:
                    self._write_column(col, '|')
                chars_written += 1
            elif seen_this and (self.expansion_row > 0):
                self._write_column(col, '\\')
                chars_written += 1
            else:
                self._write_column(col, '|')
                chars_written += 1
            self.buf += ' '
            chars_written += 1

        self._pad_horizontally(chars_written)

        # Increment self.expansion_row,
        # and move to state GraphState.COMMIT if necessary
        self.expansion_row += 1
        if self.expansion_row >= num_expansion_rows:
            self._update_state(GraphState.COMMIT)

    # Draw an octopus merge and return the number of characters written.
    def _draw_octopus_merge(self):
        # First two parents don't need dashes because their edges fit
        # neatly under the commit
        parent_stack = list(reversed(list(self._interesting_parents())[2:]))
        num_chars = 0
        while parent_stack:
            parent = parent_stack.pop()
            assert parent, 'parent is not valid'
            par_column = self._find_new_column_by_commit(parent)
            assert par_column, 'parent column not found'
            self._write_column(par_column, '-')
            num_chars += 1
            if parent_stack:
                self._write_column(par_column, '-')
                num_chars += 1
            else:
                self._write_column(par_column, '.')
        return num_chars

    def _output_commit_line(self):  # noqa: C901 pylint: disable=too-many-branches
        # Output the row containing this commit
        # Iterate up to and including self.num_columns,
        # since the current commit may not be in any of the existing
        # columns. (This happens when the current commit doesn't have any
        # children that we have already processed.)
        seen_this = False
        chars_written = 0
        for i in range(self.num_columns + 1):
            if i == self.num_columns:
                if seen_this:
                    break
                col_commit = self.commit
            else:
                col = self.columns[i]
                col_commit = self.columns[i].commit

            if col_commit == self.commit:
                seen_this = True
                self.buf += '*'
                chars_written += 1

                if self.num_parents > 2:
                    chars_written += self._draw_octopus_merge()
            elif seen_this and self.num_parents > 2:
                self._write_column(col, '\\')
                chars_written += 1
            elif seen_this and self.num_parents == 2:
                # This is a 2-way merge commit.
                # There is no GraphState.PRE_COMMIT stage for 2-way
                # merges, so this is the first line of output
                # for this commit. Check to see what the previous
                # line of output was.
                #
                # If it was GraphState.POST_MERGE, the branch line
                # coming into this commit may have been '\',
                # and not '|' or '/'. If so, output the branch
                # line as '\' on this line, instead of '|'. This
                # makes the output look nicer.
                if (self.prev_state == GraphState.POST_MERGE
                        and self.prev_commit_index < i):
                    self._write_column(col, '\\')
                else:
                    self._write_column(col, '|')
                chars_written += 1
            else:
                self._write_column(col, '|')
                chars_written += 1
            self.buf += ' '
            chars_written += 1

        self._pad_horizontally(chars_written)

        if self.num_parents > 1:
            self._update_state(GraphState.POST_MERGE)
        elif self._is_mapping_correct():
            self._update_state(GraphState.PADDING)
        else:
            self._update_state(GraphState.COLLAPSING)

    def _find_new_column_by_commit(self, commit):
        for i in range(self.num_new_columns):
            if self.new_columns[i].commit == commit:
                return self.new_columns[i]
        return None

    def _output_post_merge_line(self):
        seen_this = False
        chars_written = 0
        for i in range(self.num_columns + 1):
            if i == self.num_columns:
                if seen_this:
                    break
                col_commit = self.commit
            else:
                col = self.columns[i]
                col_commit = col.commit

            if col_commit == self.commit:
                # Since the current commit is a merge find
                # the columns for the parent commits in
                # new_columns and use those to format the
                # edges.
                seen_this = True
                parents = self._interesting_parents()
                assert parents, 'merge has no parents'
                par_column = self._find_new_column_by_commit(next(parents))
                assert par_column, 'parent column not found'
                self._write_column(par_column, '|')
                chars_written += 1
                for parent in parents:
                    assert parent, 'parent is not valid'
                    par_column = self._find_new_column_by_commit(parent)
                    assert par_column, 'parent column not found'
                    self._write_column(par_column, '\\')
                    self.buf += ' '
                chars_written += (self.num_parents - 1) * 2
            elif seen_this:
                self._write_column(col, '\\')
                self.buf += ' '
                chars_written += 2
            else:
                self._write_column(col, '|')
                self.buf += ' '
                chars_written += 2

        self._pad_horizontally(chars_written)

        if self._is_mapping_correct():
            self._update_state(GraphState.PADDING)
        else:
            self._update_state(GraphState.COLLAPSING)

    def _output_collapsing_line(self):  # noqa: C901 pylint: disable=too-many-branches
        used_horizontal = False
        horizontal_edge = -1
        horizontal_edge_target = -1

        # Clear out the new_mapping array
        for i in range(self.mapping_size):
            self.new_mapping[i] = -1

        for i in range(self.mapping_size):
            target = self.mapping[i]
            if target < 0:
                continue

            # Since update_columns() always inserts the leftmost
            # column first, each branch's target location should
            # always be either its current location or to the left of
            # its current location.
            #
            # We never have to move branches to the right. This makes
            # the graph much more legible, since whenever branches
            # cross, only one is moving directions.
            assert target * 2 <= i, \
                'position {} targetting column {}'.format(i, target * 2)

            if target * 2 == i:
                # This column is already in the correct place
                assert self.new_mapping[i] == -1
                self.new_mapping[i] = target
            elif self.new_mapping[i - 1] < 0:
                # Nothing is to the left. Move to the left by one.
                self.new_mapping[i - 1] = target
                # If there isn't already an edge moving horizontally
                # select this one.
                if horizontal_edge == -1:
                    horizontal_edge = i
                    horizontal_edge_target = target
                    # The variable target is the index of the graph
                    # column, and therefore target * 2 + 3 is the
                    # actual screen column of the first horizontal
                    # line.
                    for j in range((target * 2) + 3, i - 2, 2):
                        self.new_mapping[j] = target
            elif self.new_mapping[i - 1] == target:
                # There is a branch line to our left
                # already, and it is our target. We
                # combine with this line, since we share
                # the same parent commit.
                #
                # We don't have to add anything to the
                # output or new_mapping, since the
                # existing branch line has already taken
                # care of it.
                pass
            else:
                # There is a branch line to our left,
                # but it isn't our target. We need to
                # cross over it.
                #
                # The space just to the left of this
                # branch should always be empty.
                #
                # The branch to the left of that space
                # should be our eventual target.
                assert self.new_mapping[i - 1] > target
                assert self.new_mapping[i - 2] < 0
                assert self.new_mapping[i - 3] == target
                self.new_mapping[i - 2] = target
                # Mark this branch as the horizontal edge to
                # prevent any other edges from moving
                # horizontally.
                if horizontal_edge == -1:
                    horizontal_edge = i

        # The new mapping may be 1 smaller than the old mapping
        if self.new_mapping[self.mapping_size - 1] < 0:
            self.mapping_size -= 1

        # Output a line based on the new mapping info
        for i in range(self.mapping_size):
            target = self.new_mapping[i]
            if target < 0:
                self.buf += ' '
            elif target * 2 == i:
                self._write_column(self.new_columns[target], '|')
            elif target == horizontal_edge_target and i != horizontal_edge - 1:
                # Set the mappings for all but the
                # first segment to -1 so that they
                # won't continue into the next line.
                if i != (target * 2) + 3:
                    self.new_mapping[i] = -1
                used_horizontal = True
                self._write_column(self.new_columns[target], '_')
            else:
                if used_horizontal and i < horizontal_edge:
                    self.new_mapping[i] = -1
                self._write_column(self.new_columns[target], '/')

        self._pad_horizontally(self.mapping_size)
        self.mapping, self.new_mapping = self.new_mapping, self.mapping

        # If self.mapping indicates that all of the branch lines
        # are already in the correct positions, we are done.
        # Otherwise, we need to collapse some branch lines together.
        if self._is_mapping_correct():
            self._update_state(GraphState.PADDING)

    def _next_line(self):
        prev_state = self.state
        if self.state == GraphState.PADDING:
            self._output_padding_line()
        elif self.state == GraphState.SKIP:
            self._output_skip_line()
        elif self.state == GraphState.PRE_COMMIT:
            self._output_pre_commit_line()
        elif self.state == GraphState.COMMIT:
            self._output_commit_line()
        elif self.state == GraphState.POST_MERGE:
            self._output_post_merge_line()
        elif self.state == GraphState.COLLAPSING:
            self._output_collapsing_line()
        return prev_state == GraphState.COMMIT

    def _padding_line(self):
        """
        Output a padding line in the graph.

        This is similar to next_line(). However, it is guaranteed to
        never print the current commit line. Instead, if the commit line is
        next, it will simply output a line of vertical padding, extending the
        branch lines downwards, but leaving them otherwise unchanged.
        """
        if self.state != GraphState.COMMIT:
            self._next_line()
            return

        # Output the row containing this commit
        # Iterate up to and including self.num_columns,
        # since the current commit may not be in any of the existing
        # columns. (This happens when the current commit doesn't have any
        # children that we have already processed.)
        for i in range(self.num_columns):
            col = self.columns[i]
            self._write_column(col, '|')
            if col.commit == self.commit and self.num_parents > 2:
                self.buf += ' ' * (self.num_parents - 2) * 2
            else:
                self.buf += ' '

        self._pad_horizontally(self.num_columns)

        # Update self.prev_state since we have output a padding line
        self.prev_state = GraphState.PADDING

    def _is_commit_finished(self):
        return self.state == GraphState.PADDING

    def _show_commit(self):
        shown_commit_line = False

        # When showing a diff of a merge against each of its parents, we
        # are called once for each parent without update having been
        # called. In this case, simply output a single padding line.
        if self._is_commit_finished():
            self._show_padding()
            shown_commit_line = True

        while not shown_commit_line and not self._is_commit_finished():
            shown_commit_line = self._next_line()
            self.outfile.write(self.buf)
            if not shown_commit_line:
                self.outfile.write('\n')
            self.buf = ''

    def _show_padding(self):
        self._padding_line()
        self.outfile.write(self.buf)
        self.buf = ''

    def _show_remainder(self):
        shown = False

        if self._is_commit_finished():
            return False

        while True:
            self._next_line()
            self.outfile.write(self.buf)
            self.buf = ''
            shown = True

            if not self._is_commit_finished():
                self.outfile.write('\n')
            else:
                break

        return shown
