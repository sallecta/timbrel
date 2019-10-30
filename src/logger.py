#!/usr/bin/python3

########################################################################
#                                                                      #
# logger.py                                                            #
#                                                                      #
# Copyright (C) 2015 PJ Singh <psingh.cubic@gmail.com>                 #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# This file is part of Timbrel - Custom Ubuntu ISO Creator.              #
#                                                                      #
# Timbrel is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# Timbrel is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with Timbrel. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                      #
########################################################################

import textwrap

total_width = 80

########################################################################
# Logging Functions
########################################################################


def log_step(text):
    global total_width
    lines = textwrap.fill(
        str(text).strip(),
        width=total_width,
        initial_indent='',
        subsequent_indent='')
    lines = '{:<{}}'.format(lines, total_width)

    # print()
    # print(lines)
    print('\n%s' % lines)


def log_note(text):
    _log_note(text)
    # _log_note_ellipsis(text)


def log_data(column_a_text, column_b_text=None, sender=None):
    # _log_data_top(column_a_text, column_b_text)
    # _log_data_bottom(column_a_text, column_b_text)
    _log_data_hanging(column_a_text, column_b_text, sender)

########################################################################
# Private Logging Functions
########################################################################


def _log_note(text):
    global total_width

    lines = textwrap.fill(
        str(text).strip(),
        width=total_width,
        initial_indent='  ',
        subsequent_indent='  ')

    print(lines)


def _log_note_ellipsis(text):
    global total_width

    lines = textwrap.wrap(
        str(text).strip(),
        width=total_width,
        initial_indent='  ',
        subsequent_indent='  ')

    for index in range(len(lines)):
        if index < len(lines) - 1:
            # Case for all lines prior to the last line.
            line = '{:<{}}'.format(lines[index], total_width)
        else:
            # Case for the last line.
            line = '{:.<{}}'.format(lines[index], total_width)
        print(line)


def _log_data_top(column_a_text, column_b_text=None):
    # Column A width includes the initial/subsequent indents of four characters.
    # Column B width includes the initial/subsequent indents of one character.
    # The total width is the sum of column A width + column B width.

    global total_width
    width_column_a = int(total_width / 2.0)
    width_column_b = total_width - width_column_a

    column_a_text = str(column_a_text).strip()
    column_a_lines = textwrap.wrap(
        column_a_text,
        width=width_column_a,
        initial_indent='    ',
        subsequent_indent='    ')

    column_b_text = str(column_b_text).strip()
    if len(column_b_text) == 0: column_b_text = 'Empty'
    column_b_lines = textwrap.wrap(
        column_b_text,
        width=width_column_b,
        initial_indent=' ',
        subsequent_indent=' ')

    column_a_size = len(column_a_lines)
    column_b_size = len(column_b_lines)

    for index in range(max(column_a_size, column_b_size)):

        # Column A
        if index < column_a_size - 1:
            # Case for all lines prior to the last line.
            column_a_line = '{:<{}}'.format(
                column_a_lines[index],
                width_column_a)
        elif index == column_a_size - 1:
            # Case for the last line.
            column_a_line = '{:.<{}}'.format(
                column_a_lines[index],
                width_column_a)
        else:
            # Case for non-existent lines.
            column_a_line = ' ' * width_column_a

        # Column B
        if index < column_b_size:
            # Case for all lines prior to the last line.
            column_b_line = '{:<{}}'.format(
                column_b_lines[index],
                width_column_b)
        else:
            # Case for non-existent lines.
            column_b_line = ''

        # Print column A and column B.
        print('{}{}'.format(column_a_line, column_b_line))


def _log_data_bottom(column_a_text, column_b_text=None):
    # Column A width includes the initial/subsequent indents of four characters.
    # Column B width includes the initial/subsequent indents of one character.
    # The total width is the sum of column A width + column B width.

    global total_width
    width_column_a = int(total_width / 2.0)
    width_column_b = total_width - width_column_a

    column_a_text = str(column_a_text).strip()
    column_a_lines = textwrap.wrap(
        column_a_text,
        width=width_column_a,
        initial_indent='    ',
        subsequent_indent='    ')

    column_b_text = str(column_b_text).strip()
    if len(column_b_text) == 0: column_b_text = 'Empty'
    column_b_lines = textwrap.wrap(
        column_b_text,
        width=width_column_b,
        initial_indent=' ',
        subsequent_indent=' ')

    column_a_size = len(column_a_lines)
    column_b_size = len(column_b_lines)
    column_b_start = (column_a_size -
                      column_b_size) * (column_a_size > column_b_size)

    for index in range(max(column_a_size, column_b_size)):

        # Column A
        if index < column_a_size - 1:
            # Case for all lines prior to the last line.
            column_a_line = '{:<{}}'.format(
                column_a_lines[index],
                width_column_a)
        elif index == column_a_size - 1:
            # Case for the last line.
            column_a_line = '{:.<{}}'.format(
                column_a_lines[index],
                width_column_a)
        else:
            # Case for non-existent lines.
            column_a_line = ' ' * width_column_a

        # Column B
        if index >= column_b_start:
            # Case for all lines including the last line.
            column_b_line = '{:<{}}'.format(
                column_b_lines[index - column_b_start],
                width_column_b)
        else:
            # Case for non-existent lines.
            column_b_line = ''

        # Print column A and column B.
        print('{}{}'.format(column_a_line, column_b_line))


def _log_data_hanging(column_a_text, column_b_text=None, sender=None):
    # Column A width includes the initial/subsequent indents of four characters.
    # Column B width includes the initial/subsequent indents of one character.
    # The total width is the sum of column A width + column B width.

    global total_width
    width_column_a = int(total_width / 2.0)
    width_column_b = total_width - width_column_a

    column_a_text = str(column_a_text).strip()
    column_a_lines = textwrap.wrap(
        column_a_text,
        width=width_column_a,
        initial_indent='    ',
        subsequent_indent='    ')

    column_b_text = str(column_b_text).strip()
    if len(column_b_text) == 0: column_b_text = 'Empty'
    column_b_lines = textwrap.wrap(
        column_b_text,
        width=width_column_b,
        initial_indent='... ',
        subsequent_indent='    ')

    column_a_size = len(column_a_lines)
    column_b_size = len(column_b_lines)
    column_b_start = column_a_size - 1

    for index in range(column_a_size + column_b_size - 1):

        # Column A
        if index < column_a_size - 1:
            # Case for all lines prior to the last line.
            column_a_line = '{:<{}}'.format(
                column_a_lines[index],
                width_column_a)
        elif index == column_a_size - 1:
            # Case for the last line.
            column_a_line = '{:.<{}}'.format(
                column_a_lines[index],
                width_column_a)
        else:
            # Case for non-existent lines.
            column_a_line = ' ' * width_column_a

        # Column B
        if index >= column_b_start:
            # Case for all lines including the last line.
            column_b_line = '{:<{}}'.format(
                column_b_lines[index - column_b_start],
                width_column_b)
        else:
            # Case for non-existent lines.
            column_b_line = ''

        # Print column A and column B.
        print('{}{}'.format(column_a_line, column_b_line))
