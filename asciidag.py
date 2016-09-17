#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class Column(object):
    """A single column of output

    Attributes:
        commit -- The parent commit of this column.
        color -- The color to (optionally) print this column in.  This is an index into column_colors.
    """
    def __init__(self, commit, color):
        self.commit = commit
        self.color = color

# enum graph_state {
#         GRAPH_PADDING,
#         GRAPH_SKIP,
#         GRAPH_PRE_COMMIT,
#         GRAPH_COMMIT,
#         GRAPH_POST_MERGE,
#         GRAPH_COLLAPSING
# };

class Graph(object):
# struct git_graph {
#     /*
#     * The commit currently being processed
#     */
#     struct commit *commit
#     /* The rev-info used for the current traversal */
#     struct rev_info *revs
#     /*
#     * The number of interesting parents that this commit has.
#     *
#     * Note that this is not the same as the actual number of parents.
#     * This count excludes parents that won't be printed in the graph
#          * output, as determined by is_interesting().
#          */
#         int num_parents
#         /*
#          * The width of the graph output for this commit.
#          * All rows for this commit are padded to this width, so that
#          * messages printed after the graph output are aligned.
#          */
#         int width
#         /*
#          * The next expansion row to print
#          * when state is GRAPH_PRE_COMMIT
#          */
#         int expansion_row
#         /*
#          * The current output state.
#          * This tells us what kind of line next_line() should output.
#          */
#         enum graph_state state
#         /*
#          * The output state for the previous line of output.
#          * This is primarily used to determine how the first merge line
#          * should appear, based on the last line of the previous commit.
#          */
#         enum graph_state prev_state
#         /*
#          * The index of the column that refers to this commit.
#          *
#          * If none of the incoming columns refer to this commit,
#          * this will be equal to num_columns.
#          */
#         int commit_index
#         /*
#          * The commit_index for the previously displayed commit.
#          *
#          * This is used to determine how the first line of a merge
#          * graph output should appear, based on the last line of the
#          * previous commit.
#          */
#         int prev_commit_index
#         /*
#          * The maximum number of columns that can be stored in the columns
#          * and new_columns arrays.  This is also half the number of entries
#          * that can be stored in the mapping and new_mapping arrays.
#          */
#         int column_capacity
#         /*
#          * The number of columns (also called "branch lines" in some places)
#          */
#         int num_columns
#         /*
#          * The number of columns in the new_columns array
#          */
#         int num_new_columns
#         /*
#          * The number of entries in the mapping array
#          */
#         int mapping_size
#         /*
#          * The column state before we output the current commit.
#          */
#         struct column *columns
#         /*
#          * The new column state after we output the current commit.
#          * Only valid when state is GRAPH_COLLAPSING.
#          */
#         struct column *new_columns
#         /*
#          * An array that tracks the current state of each
#          * character in the output line during state GRAPH_COLLAPSING.
#          * Each entry is -1 if this character is empty, or a non-negative
#          * integer if the character contains a branch line.  The value of
#          * the integer indicates the target position for this branch line.
#          * (I.e., this array maps the current column positions to their
#          * desired positions.)
#          *
#          * The maximum capacity of this array is always
#          * sizeof(int) * 2 * column_capacity.
#          */
#         int *mapping
#         /*
#          * A temporary array for computing the next mapping state
#          * while we are outputting a mapping line.  This is stored as part
#          * of the git_graph simply so we don't have to allocate a new
#     * temporary array each time we have to output a collapsing line.
#     */
#     int *new_mapping
#     /*
#     * The current default column color being used.  This is
#     * stored as an index into the array column_colors.
#     */
#     unsigned short default_column_color

    def strbuf_write_column(sb, c, col_char):
        if c.color is not None:
            strbuf_addstr(sb, colors[c.color])
        strbuf_addch(sb, col_char)
        if c.color is not None:
            strbuf_addstr(sb, colors[-1])


    def __init__(self, opt, column_colors=None):
        self.column_colors = colors

        if column_colors is None:
            self.column_colors = COLUMN_COLORS_ANSI
                                    
        self.commit = None
        self.revs = opt
        self.num_parents = 0
        self.expansion_row = 0
        self.state = GRAPH_PADDING
        self.prev_state = GRAPH_PADDING
        self.commit_index = 0
        self.prev_commit_index = 0
        self.num_columns = 0
        self.num_new_columns = 0
        self.mapping_size = 0
        # Start the column color at the maximum value, since we'll
        # always increment it for the first commit we output.
        # This way we start at 0 for the first commit.
        self.default_column_color = len(column_colors) - 1

        self.columns = []
        self.new_columns = []
        self.mapping = []
        self.new_mapping = []

    def update_state(self, s):
        self.prev_state = self.state
        self.state = s

    def is_interesting(self, commit):
        """Returns True if the commit will be printed in the graph output"""
        # /*
        #  * If revs->boundary is set, commits whose children have
        #  * been shown are always interesting, even if they have the
        #  * UNINTERESTING or TREESAME flags set.
        #  */
        if self.revs and self.revs.boundary:
            if commit.object.flags & CHILD_SHOWN:
                return False

        # /*
        #  * Otherwise, use get_commit_action() to see if this commit is
        #  * interesting
        #  */
        return get_commit_action(graph.revs, commit) == commit_show

    def next_interesting_parent(self, orig):
        #     /*
        # * If revs.first_parent_only is set, only the first
        # * parent is interesting.  None of the others are.
        # */
        if self.revs.first_parent_only:
            return None

        #     /*
        # * Return the next interesting commit after orig
        # */
        for item in iter(orig):
            if self.is_interesting(item):
                    return item

        return None


    def first_interesting_parent(self):
        parents = self.commit.parents

        #     /*
        # * If this commit has no parents, ignore it
        # */
        if parents is None:
            return None

        #     /*
        # * If the first parent is interesting, return it
        # */
        if self.is_interesting(parents[0].item):
            return parents

        #     /*
        # * Otherwise, call next_interesting_parent() to get
        # * the next interesting parent
        # */
        return self.next_interesting_parent()


    def get_current_column_color(self):
        if not want_color(self.revs.diffopt.use_color):
            return None
        return self.default_column_color

    # /*
    # * Update the graph's default column color.
    #  */
    def increment_column_color(self):
        self.default_column_color = (self.default_column_color + 1) % column_colors_max

    def find_commit_color(self, commit):
        for i in range(self.num_columns):
            if self.columns[i].commit == commit:
                return self.columns[i].color
        return self.get_current_column_color(graph)

    def insert_into_new_columns(self, commit, mapping_index):
        #         /*
        #          * If the commit is already in the new_columns list, we don't need to
        # * add it.  Just update the mapping correctly.
        # */
        for i in range(self.new_columns):
            if self.new_columns[i].commit == commit:
                self.mapping[mapping_index] = i
                mapping_index += 2
                return

        # /*
        # * This commit isn't already in new_columns.  Add it.
        #  */
        self.new_columns[self.num_new_columns].commit = commit
        self.new_columns[self.num_new_columns].color = self.find_commit_color(commit)
        self.mapping[mapping_index] = self.num_new_columns
        mapping_index += 2
        self.num_new_columns += 1

    def update_width(self, is_commit_in_existing_columns):
        # /*
        #  * Compute the width needed to display the graph for this commit.
        #  * This is the maximum width needed for any row.  All other rows
        #  * will be padded to this width.
        #  *
        #  * Compute the number of columns in the widest row:
        #  * Count each existing column (self.num_columns), and each new
        #  * column added by this commit.
        #  */
        max_cols = self.num_columns + self.num_parents

        # /*
        #  * Even if the current commit has no parents to be printed, it
        #  * still takes up a column for itself.
        #  */
        if self.num_parents < 1:
            max_cols += 1

        # /*
        #  * We added a column for the current commit as part of
        #  * self.num_parents.  If the current commit was already in
        #  * self.columns, then we have double counted it.
        #  */
        if is_commit_in_existing_columns:
            max_cols -= 1

        # /*
        #  * Each column takes up 2 spaces
        #  */
        self.width = max_cols * 2

    def update_columns(self):
        parent
        tmp_columns
        max_new_columns
        mapping_idx
        i, seen_this, is_commit_in_columns

        # /*
        #  * Swap self.columns with self.new_columns
        #  * self.columns contains the state for the previous commit,
        #  * and new_columns now contains the state for our commit.
        #  *
        #  * We'll re-use the old columns array as storage to compute the new
        # * columns list for the commit after this one.
        # */
        tmp_columns = self.columns
        self.columns = self.new_columns
        self.num_columns = self.num_new_columns

        self.new_columns = tmp_columns
        self.num_new_columns = 0

        # /*
        # * Now update new_columns and mapping with the information for the
        # * commit after this one.
        # *
        # * First, make sure we have enough room.  At most, there will
        # * be self.num_columns + self.num_parents columns for the next
        # * commit.
        # */
        max_new_columns = self.num_columns + self.num_parents
        self.ensure_capacity(max_new_columns)

        # /*
        # * Clear out self.mapping
        # */
        self.mapping_size = 2 * max_new_columns
        for i in range(self.mapping_size):
            self.mapping[i] = -1

            # /*
            # * Populate self.new_columns and self.mapping
            # *
            # * Some of the parents of this commit may already be in
            # * self.columns.  If so, self.new_columns should only contain a
            # * single entry for each such commit.  self.mapping should
            # * contain information about where each current branch line is
            # * supposed to end up after the collapsing is performed.
            # */
            seen_this = False
            mapping_idx = 0
            is_commit_in_columns = True
            for i in range(self.num_columns + 1):
                col_commit
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
                        for parent in self.interesting_parents():
                            # /*
                            # * If this is a merge, or the start of a new
                            # * childless column, increment the current
                            # * color.
                            # */
                            if self.num_parents > 1 or not is_commit_in_columns:
                                self.increment_column_color()
                            self.insert_into_new_columns(
                                parent.item,
                                mapping_idx)
                        # /*
                        # * We always need to increment mapping_idx by at
                        # * least 2, even if it has no interesting parents.
                        # * The current commit always takes up at least 2
                        # * spaces.
                        # */
                        if mapping_idx == old_mapping_idx:
                            mapping_idx += 2
                else:
                    self.insert_into_new_columns(col_commit, mapping_idx)

        # /*
        # * Shrink mapping_size to be the minimum necessary
        # */
        while self.mapping_size > 1 and self.mapping[self.mapping_size - 1] < 0:
            self.mapping_size -= 1

        # /*
        # * Compute self.width for this commit
        # */
        self.update_width(is_commit_in_columns)

    def update(self, commit):
        #     /*
        # * Set the new commit
        # */
        self.commit = commit

        #     /*
        # * Count how many interesting parents this commit has
        # */
        self.num_parents = len(self.interesting_parents())

        #     /*
        # * Store the old commit_index in prev_commit_index.
        # * update_columns() will update self.commit_index for this
        # * commit.
        # */
        self.prev_commit_index = self.commit_index

        #     /*
        # * Call update_columns() to update
        # * columns, new_columns, and mapping.
        # */
        self.update_columns()

        self.expansion_row = 0

        # /*
        # * Update self.state.
        # * Note that we don't call update_state() here, since
        #      * we don't want to update self.prev_state.  No line for
        # * self.state was ever printed.
        # *
        # * If the previous commit didn't get to the GRAPH_PADDING state,
        #      * it never finished its output.  Goto GRAPH_SKIP, to print out
        #      * a line to indicate that portion of the graph is missing.
        #      *
        #      * If there are 3 or more parents, we may need to print extra rows
        #      * before the commit, to expand the branch lines around it and make
        #      * room for it.  We need to do this only if there is a branch row
        #      * (or more) to the right of this commit.
        #      *
        #      * If there are less than 3 parents, we can immediately print the
        #      * commit line.
        #      */
        if self.state != GRAPH_PADDING:
                self.state = GRAPH_SKIP
        elif self.num_parents >= 3 and self.commit_index < (self.num_columns - 1):
                self.state = GRAPH_PRE_COMMIT
        else:
                self.state = GRAPH_COMMIT

    def is_mapping_correct(self):
        # /*
        #  * The mapping is up to date if each entry is at its target,
        #  * or is 1 greater than its target.
        #  * (If it is 1 greater than the target, '/' will be printed, so it
        #  * will look correct on the next row.)
        #  */
        for i in range(self.mapping_size):
            target = self.mapping[i]
            if target < 0:
                    continue
            if target == (i / 2):
                    continue
            return False

        return True

    def pad_horizontally(self, sb, chars_written):
        # /*
        #  * Add additional spaces to the end of the strbuf, so that all
        #  * lines for a particular commit have the same width.
        #  *
        #  * This way, fields printed to the right of the graph will remain
        #  * aligned for the entire commit.
        #  */
        if chars_written >= self.width:
            return

        extra = self.width - chars_written
        strbuf_addf(sb, "%*s", extra, "")

    def output_padding_line(self, sb):
        # /*
        #  * We could conceivable be called with a NULL commit
        #  * if our caller has a bug, and invokes next_line()
        #  * immediately after init(), without first calling
        #  * update().  Return without outputting anything in this
        #  * case.
        #  */
        if self.commit is None:
            return

        # /*
        #  * Output a padding row, that leaves all branch lines unchanged
        #  */
        for i in range(self.num_new_columns):
            strbuf_write_column(sb, self.new_columns[i], '|')
            strbuf_addch(sb, ' ')

        self.pad_horizontally(sb, self.num_new_columns * 2)

    def width(self):
        return self.width

    def output_skip_line(self, sb):
        # /*
        #  * Output an ellipsis to indicate that a portion
        #  * of the graph is missing.
        #  */
        strbuf_addstr(sb, "...")
        self.pad_horizontally(sb, 3)

        if self.num_parents >= 3 and self.commit_index < (self.num_columns - 1):
                self.update_state(GRAPH_PRE_COMMIT)
        else:
                self.update_state(GRAPH_COMMIT)


    def output_pre_commit_line(self, sb):
        # /*
        #  * This function formats a row that increases the space around a commit
        #  * with multiple parents, to make room for it.  It should only be
        #  * called when there are 3 or more parents.
        #  *
        #  * We need 2 extra rows for every parent over 2.
        #  */
        assert(self.num_parents >= 3)
        num_expansion_rows = (self.num_parents - 2) * 2

        # /*
        #  * self.expansion_row tracks the current expansion row we are on.
        #  * It should be in the range [0, num_expansion_rows - 1]
        #  */
        assert(0 <= self.expansion_row and
               self.expansion_row < num_expansion_rows)

        # /*
        #  * Output the row
        #  */
        seen_this = False
        chars_written = 0
        for i in range(self.num_columns):
                col = self.columns[i]
                if col.commit == self.commit:
                        seen_this = True
                        strbuf_write_column(sb, col, '|')
                        strbuf_addf(sb, "%*s", self.expansion_row, "")
                        chars_written += 1 + self.expansion_row
                elif seen_this and (self.expansion_row == 0):
                        # /*
                        #  * This is the first line of the pre-commit output.
                        #  * If the previous commit was a merge commit and
                        #  * ended in the GRAPH_POST_MERGE state, all branch
                        #  * lines after self.prev_commit_index were
                        #  * printed as "\" on the previous line.  Continue
                        #  * to print them as "\" on this line.  Otherwise,
                        #  * print the branch lines as "|".
                        #  */
                        if self.prev_state == GRAPH_POST_MERGE and self.prev_commit_index < i:
                                strbuf_write_column(sb, col, '\\')
                        else:
                                strbuf_write_column(sb, col, '|')
                        chars_written += 1
                elif seen_this and (self.expansion_row > 0):
                        strbuf_write_column(sb, col, '\\')
                        chars_written += 1
                else:
                        strbuf_write_column(sb, col, '|')
                        chars_written += 1
                strbuf_addch(sb, ' ')
                chars_written += 1

        self.pad_horizontally(sb, chars_written)

        # /*
        #  * Increment self.expansion_row,
        #  * and move to state GRAPH_COMMIT if necessary
        #  */
        self.expansion_row += 1
        if self.expansion_row >= num_expansion_rows:
                self.update_state(GRAPH_COMMIT)

    def output_commit_char(self, sb):
        # /*
        #  * For boundary commits, print 'o'
        #  * (We should only see boundary commits when revs.boundary is set.)
        #  */
        if self.commit.object.flags & BOUNDARY:
                assert(self.revs.boundary)
                strbuf_addch(sb, 'o')
                return

        # /*
        #  * get_revision_mark() handles all other cases without assert()
        #  */
        strbuf_addstr(sb, get_revision_mark(self.revs, self.commit))


    # /*
    #  * Draw an octopus merge and return the number of characters written.
    #  */
    def draw_octopus_merge(self,
                           sb):
        #     /*
        #      * Here dashless_commits represents the number of parents
        #      * which don't need to have dashes (because their edges fit
        #                                         * neatly under the commit).
        # */
        dashless_commits = 2
        num_dashes = ((self.num_parents - dashless_commits) * 2) - 1
        for i in range(num_dashes):
            col_num = (i / 2) + dashless_commits + self.commit_index
            strbuf_write_column(sb, self.new_columns[col_num], '-')
        col_num = (i / 2) + dashless_commits + self.commit_index
        strbuf_write_column(sb, self.new_columns[col_num], '.')
        return num_dashes + 1


    def output_commit_line(self, sb):
        #     /*
        # * Output the row containing this commit
        # * Iterate up to and including self.num_columns,
        # * since the current commit may not be in any of the existing
        # * columns.  (This happens when the current commit doesn't have any
        #      * children that we have already processed.)
        #      */
        seen_this = False
        chars_written = 0
        for i in range(self.num_columns + 1):
                col = self.columns[i]
                if i == self.num_columns:
                        if seen_this:
                                break
                        col_commit = self.commit
                else:
                        col_commit = self.columns[i].commit

                if col_commit == self.commit:
                        seen_this = True
                        self.output_commit_char(sb)
                        chars_written += 1

                        if self.num_parents > 2:
                                chars_written += self.draw_octopus_merge(
                                                                          sb)
                elif seen_this and (self.num_parents > 2):
                        strbuf_write_column(sb, col, '\\')
                        chars_written += 1
                elif seen_this and (self.num_parents == 2):
                 #        /*
                 #         * This is a 2-way merge commit.
                 #         * There is no GRAPH_PRE_COMMIT stage for 2-way
                 #         * merges, so this is the first line of output
                 #         * for this commit.  Check to see what the previous
                 #         * line of output was.
                 #         *
                 #         * If it was GRAPH_POST_MERGE, the branch line
                 #         * coming into this commit may have been '\',
                 # * and not '|' or '/'.  If so, output the branch
                 # * line as '\' on this line, instead of '|'.  This
                 #         * makes the output look nicer.
                 #         */
                        if self.prev_state == GRAPH_POST_MERGE and self.prev_commit_index < i:
                                strbuf_write_column(sb, col, '\\')
                        else:
                                strbuf_write_column(sb, col, '|')
                        chars_written += 1
                else:
                        strbuf_write_column(sb, col, '|')
                        chars_written += 1
                strbuf_addch(sb, ' ')
                chars_written += 1

        self.pad_horizontally(sb, chars_written)

        # /*
        #  * Update self.state
        #  */
        if self.num_parents > 1:
                self.update_state(GRAPH_POST_MERGE)
        elif self.is_mapping_correct():
                self.update_state(GRAPH_PADDING)
        else:
                self.update_state(GRAPH_COLLAPSING)


    def find_new_column_by_commit(self, commit):
        for i in range(self.num_new_columns):
                if self.new_columns[i].commit == commit:
                        return self.new_columns[i]
        return None


    def output_post_merge_line(self, sb):
        seen_this = False

        # /*
        #  * Output the post-merge row
        #  */
        chars_written = 0
        for i in range(self.num_columns + 1):
            col = self.columns[i]
            if i == self.num_columns:
                    if seen_this:
                            break
                    col_commit = self.commit
            else:
                    col_commit = col.commit

            if col_commit == self.commit:
                    # /*
                    #  * Since the current commit is a merge find
                    #  * the columns for the parent commits in
                    #  * new_columns and use those to format the
                    #  * edges.
                    #  */
                    seen_this = True
                    parent = self.first_interesting_parent()
                    assert(parent)
                    par_column = self.find_new_column_by_commit(parent.item)
                    assert(par_column)

                    strbuf_write_column(sb, par_column, '|')
                    chars_written += 1
                    for j in range(self.num_parents - 1):
                            parent = self.next_interesting_parent(parent)
                            assert(parent)
                            par_column = self.find_new_column_by_commit(parent.item)
                            assert(par_column)
                            strbuf_write_column(sb, par_column, '\\')
                            strbuf_addch(sb, ' ')
                    chars_written += j * 2
            elif seen_this:
                    strbuf_write_column(sb, col, '\\')
                    strbuf_addch(sb, ' ')
                    chars_written += 2
            else:
                    strbuf_write_column(sb, col, '|')
                    strbuf_addch(sb, ' ')
                    chars_written += 2

            self.pad_horizontally(sb, chars_written)

            # /*
            #  * Update self.state
            #  */
            if self.is_mapping_correct():
                    self.update_state(GRAPH_PADDING)
            else:
                    self.update_state(GRAPH_COLLAPSING)


    def output_collapsing_line(self, sb):
        used_horizontal = False
        horizontal_edge = -1
        horizontal_edge_target = -1

        # /*
        #  * Clear out the new_mapping array
        #  */
        for i in range(self.mapping_size):
                self.new_mapping[i] = -1

        for i in range(self.mapping_size):
                target = self.mapping[i]
                if target < 0:
                        continue

                # /*
                #  * Since update_columns() always inserts the leftmost
                #  * column first, each branch's target location should
                #  * always be either its current location or to the left of
                #  * its current location.
                #  *
                #  * We never have to move branches to the right.  This makes
                #  * the graph much more legible, since whenever branches
                #  * cross, only one is moving directions.
                #  */
                assert(target * 2 <= i)

                if target * 2 == i:
                        # /*
                        # * This column is already in the
                        # * correct place
                        # */
                        assert(self.new_mapping[i] == -1)
                        self.new_mapping[i] = target
                elif self.new_mapping[i - 1] < 0:
                    # /*
                    # * Nothing is to the left.
                    # * Move to the left by one
                    # */
                    self.new_mapping[i - 1] = target
                    # /*
                    # * If there isn't already an edge moving horizontally
                    #      * select this one.
                    #      */
                    if horizontal_edge == -1:
                        horizontal_edge = i
                        horizontal_edge_target = target
                        # /*
                        #  * The variable target is the index of the graph
                        #  * column, and therefore target * 2 + 3 is the
                        #  * actual screen column of the first horizontal
                        #  * line.
                        #  */
                        for j in range((target * 2) + 3, i - 2, 2):
                                self.new_mapping[j] = target
                elif self.new_mapping[i - 1] == target:
                    #     /*
                    #      * There is a branch line to our left
                    #      * already, and it is our target.  We
                    #      * combine with this line, since we share
                    #      * the same parent commit.
                    #      *
                    #      * We don't have to add anything to the
                    # * output or new_mapping, since the
                    # * existing branch line has already taken
                    # * care of it.
                    # */
                    pass
                else:
                    # /*
                    # * There is a branch line to our left,
                    # * but it isn't our target.  We need to
                    #      * cross over it.
                    #      *
                    #      * The space just to the left of this
                    #      * branch should always be empty.
                    #      *
                    #      * The branch to the left of that space
                    #      * should be our eventual target.
                    #      */
                        assert(self.new_mapping[i - 1] > target)
                        assert(self.new_mapping[i - 2] < 0)
                        assert(self.new_mapping[i - 3] == target)
                        self.new_mapping[i - 2] = target
                        # /*
                        #  * Mark this branch as the horizontal edge to
                        #  * prevent any other edges from moving
                        #  * horizontally.
                        #  */
                        if horizontal_edge == -1:
                                horizontal_edge = i

        # /*
        #  * The new mapping may be 1 smaller than the old mapping
        #  */
        if self.new_mapping[self.mapping_size - 1] < 0:
            self.mapping_size -= 1

        # /*
        #  * Output out a line based on the new mapping info
        #  */
        for i in range(self.mapping_size):
                target = self.new_mapping[i]
                if target < 0:
                        strbuf_addch(sb, ' ')
                elif target * 2 == i:
                        strbuf_write_column(sb, self.new_columns[target], '|')
                elif target == horizontal_edge_target and i != horizontal_edge - 1:
                    #             /*
                    #              * Set the mappings for all but the
                    #              * first segment to -1 so that they
                    #              * won't continue into the next line.
                    # */
                    if i != (target * 2) + 3:
                        self.new_mapping[i] = -1
                    used_horizontal = True
                    strbuf_write_column(sb, self.new_columns[target], '_')
                else:
                    if used_horizontal and i < horizontal_edge:
                        self.new_mapping[i] = -1
                    strbuf_write_column(sb, self.new_columns[target], '/')

        self.pad_horizontally(sb, self.mapping_size)

        #     /*
        # * Swap mapping and new_mapping
        # */
        tmp_mapping = self.mapping
        self.mapping = self.new_mapping
        self.new_mapping = tmp_mapping

        #     /*
        # * If self.mapping indicates that all of the branch lines
        # * are already in the correct positions, we are done.
        # * Otherwise, we need to collapse some branch lines together.
        # */
        if self.is_mapping_correct():
            self.update_state(GRAPH_PADDING)

    def next_line(self, sb):
        if self.state == GRAPH_PADDING:
            self.output_padding_line(sb)
            return False
        elif self.state == GRAPH_SKIP:
            self.output_skip_line(sb)
            return False
        elif self.state == GRAPH_PRE_COMMIT:
            self.output_pre_commit_line(sb)
            return False
        elif self.state == GRAPH_COMMIT:
            self.output_commit_line(sb)
            return True
        elif self.state == GRAPH_POST_MERGE:
            self.output_post_merge_line(sb)
            return False
        elif self.state == GRAPH_COLLAPSING:
            self.output_collapsing_line(sb)
            return False
        else:
            return False

    """
    Output a padding line in the graph.
    This is similar to next_line().  However, it is guaranteed to
    never print the current commit line.  Instead, if the commit line is
    next, it will simply output a line of vertical padding, extending the
    branch lines downwards, but leaving them otherwise unchanged.
    """
    def padding_line(self, sb):
        if self.state != GRAPH_COMMIT:
                self.next_line(sb)
                return

        #     /*
        # * Output the row containing this commit
        # * Iterate up to and including self.num_columns,
        # * since the current commit may not be in any of the existing
        # * columns.  (This happens when the current commit doesn't have any
        #      * children that we have already processed.)
        #      */
        for i in range(self.num_columns):
                col = self.columns[i]
                strbuf_write_column(sb, col, '|')
                if col.commit == self.commit and self.num_parents > 2:
                        strbuf_addchars(sb, ' ', (self.num_parents - 2) * 2)
                else:
                        strbuf_addch(sb, ' ')

        self.pad_horizontally(sb, self.num_columns)

        # /*
        #  * Update self.prev_state since we have output a padding line
        #  */
        self.prev_state = GRAPH_PADDING


    def is_commit_finished(self):
        return (self.state == GRAPH_PADDING)


    def show_commit(self):
        msgbuf = STRBUF_INIT
        shown_commit_line = False

        self.show_line_prefix(default_diffopt)

        # /*
        #  * When showing a diff of a merge against each of its parents, we
        #  * are called once for each parent without update having been
        #  * called.  In this case, simply output a single padding line.
        #  */
        if self.is_commit_finished():
                self.graph_show_padding()
                shown_commit_line = True

        while not shown_commit_line and not self.is_commit_finished():
                shown_commit_line = self.next_line(msgbuf)
                fwrite(msgbuf.buf, sizeof(char), msgbuf.len,
                        self.revs.diffopt.file)
                if not shown_commit_line:
                        putc('\n', self.revs.diffopt.file)
                        self.show_line_prefix(self.revs.diffopt)
                strbuf_setlen(msgbuf, 0)

        strbuf_release(msgbuf)


    def show_oneline(self):
        msgbuf = STRBUF_INIT

        self.next_line(msgbuf)
        fwrite(msgbuf.buf, sizeof(char), msgbuf.len, self.revs.diffopt.file)
        strbuf_release(msgbuf)


    def show_padding(self):
        msgbuf = STRBUF_INIT

        self.padding_line(msgbuf)
        fwrite(msgbuf.buf, sizeof(char), msgbuf.len, self.revs.diffopt.file)
        strbuf_release(msgbuf)


    def show_remainder(self):
        msgbuf = STRBUF_INIT
        shown = False

        if self.is_commit_finished():
                return False

        while True:
                self.next_line(msgbuf)
                fwrite(msgbuf.buf, sizeof(char), msgbuf.len,
                        self.revs.diffopt.file)
                strbuf_setlen(msgbuf, 0)
                shown = True

                if not self.is_commit_finished():
                        putc('\n', self.revs.diffopt.file)
                        self.show_line_prefix(self.revs.diffopt)
                else:
                        break
        strbuf_release(msgbuf)

        return shown


# /*
#  * Print a strbuf.  If the graph is non-NULL, all lines but the first will be
#  * prefixed with the graph output.
#  *
#  * If the strbuf ends with a newline, the output will end after this
#  * newline.  A new graph line will not be printed after the final newline.
#  * If the strbuf is empty, no output will be printed.
#  *
#  * Since the first line will not include the graph output, the caller is
#  * responsible for printing this line's graph (perhaps via
#                                                * show_commit() or show_oneline()) before calling
#                  * show_strbuf().
#                  *
#                  * Note that unlike some other graph display functions, you must pass the file
#                  * handle directly. It is assumed that this is the same file handle as the
#                  * file specified by the graph diff options. This is necessary so that
#                  * show_strbuf can be called even with a NULL graph.
#                  */
    def show_strbuf(self, file, sb):
        # /*
        #              * Print the strbuf line by line,
        #              * and display the graph info before each line but the first.
        #              */
        p = sb.buf
        while p:
            next_p = strchr(p, '\n')
            if next_p:
                    next_p += 1
                    len = next_p - p
            else:
                len = (sb.buf + sb.len) - p
            fwrite(p, sizeof(char), len, file)
            if next_p:
                self.show_oneline()
                p = next_p

    def show_commit_msg(self, file, sb):
        # /*
        #              * Show the commit message
        #              */
        self.show_strbuf(file, sb)

        newline_terminated = (sb.len and sb.buf[sb.len - 1] == '\n')

        # /*
        #              * If there is more output needed for this commit, show it now
        #              */
        if not self.is_commit_finished():
            # /*
            # * If sb doesn't have a terminating newline, print one now,
            #  * so we can start the remainder of the graph output on a
            #  * new line.
            #  */
            if not newline_terminated:
                    putc('\n', file)

            self.show_remainder()

            # /*
            #  * If sb ends with a newline, our output should too.
            #  */
            if newline_terminated:
                    putc('\n', file)
