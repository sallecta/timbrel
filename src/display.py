#!/usr/bin/python3

########################################################################
#                                                                      #
# display.py                                                           #
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
me='display.py'
import timbrel_cfg

import logger
import timbrel_log

import model

import gi
gi.require_version('Gtk', '3.0')
# gi.require_version('GtkSource', '3.0')
try:
    gi.require_version('GtkSource', '4')
    timbrel_log.info(me,'Using GtkSource version', '4')
except ValueError:
    gi.require_version('GtkSource', '3.0')
    timbrel_log.info(me,'Using GtkSource version', '3.0')
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import GtkSource
import os
import time

########################################################################
# Constants
########################################################################

# Status
OK = 0
ERROR = 1
OPTIONAL = 2
BULLET = 3
PROCESSING = 4

# Icons corresponding to status
icons = [
    'timbrel-ok',
    'timbrel-error',
    'timbrel-optional',
    'timbrel-bullet',
    'timbrel-blank'
]

########################################################################
# Functions
########################################################################


def get_theme_style(window):

    style_context = window.get_style_context()

    # Foreground

    foreground_red = style_context.get_color(Gtk.StateFlags.NORMAL).red
    foreground_green = style_context.get_color(Gtk.StateFlags.NORMAL).green
    foreground_blue = style_context.get_color(Gtk.StateFlags.NORMAL).blue

    # logger.log_data('foreground_red', foreground_red)
    # logger.log_data('foreground_green', foreground_green)
    # logger.log_data('foreground_blue', foreground_blue)

    foreground_average = (
        foreground_red + foreground_green + foreground_blue) / 256
    # logger.log_data('The average foreground color is', foreground_average)

    # Background

    background_red = style_context.get_background_color(
        Gtk.StateFlags.NORMAL).red
    background_green = style_context.get_background_color(
        Gtk.StateFlags.NORMAL).green
    background_blue = style_context.get_background_color(
        Gtk.StateFlags.NORMAL).blue

    # logger.log_data('background_red', background_red)
    # logger.log_data('background_green', background_green)
    # logger.log_data('background_blue', background_blue)

    background_average = (
        background_red + background_green + background_blue) / 256
    # logger.log_data('The average background color is', background_average)

    theme_style = 'unknown'
    if (foreground_average > background_average):
        theme_style = 'dark'
    else:
        theme_style = 'light'

    return theme_style


def update_icon_path(theme_style):

    icon_theme = Gtk.IconTheme.get_default()

    timbrel_log.info(me,'Set icon theme search path.')
    # icon_theme.set_search_path(model.default_icon_theme_search_path)
    icon_search_path = timbrel_cfg.path + '/icons'    
    
    Gtk.IconTheme.set_search_path(icon_theme,[icon_search_path])
    
    icon_theme_search_path = icon_theme.get_search_path()
    timbrel_log.info(me, 'new Icon theme search path', icon_theme.get_search_path())


def set_column_visible(widget_name, is_visible):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.TreeViewColumn.set_visible, widget, is_visible)


def show(widget_name):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.Widget.show, widget)


def hide(widget_name):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.Widget.hide, widget)


# def hide_on_delete(widget_name):
#     widget = model.builder.get_object(widget_name)
#     GLib.idle_add(Gtk.Widget.hide_on_delete, widget)


def set_visible(widget_name, is_visible):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.Widget.set_visible, widget, is_visible)


def set_solid(widget_name, is_solid):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.Widget.set_opacity, widget, is_solid)


def set_sensitive(widget_name, is_sensitive):
    widget = model.builder.get_object(widget_name)
    GLib.idle_add(Gtk.Widget.set_sensitive, widget, is_sensitive)


def set_label_error(widget_name, is_error):
    # logger.log_data('Set name property to error is "%s" for label' % is_error, widget_name)
    label = model.builder.get_object(widget_name)
    name = label.get_name()
    # logger.log_data('The current name for the label is', name)
    if is_error:
        if name == 'normal':
            label.set_name('error')
            # GLib.idle_add(Gtk.Label.set_name, label, 'error')
        elif name == 'error':
            pass
        elif name == 'non-editable':
            label.set_name('non-editable-error')
            # GLib.idle_add(Gtk.Label.set_name, label, 'non-editable-error')
        elif name == 'non-editable-error':
            pass
        elif name == 'automatic':
            label.set_name('automatic-error')
            # GLib.idle_add(Gtk.Label.set_name, label, 'automatic-error')
        elif name == 'automatic-error':
            pass
        elif name == 'automatic-non-editable':
            label.set_name('automatic-non-editable-error')
            # GLib.idle_add(Gtk.Label.set_name, label, 'automatic-non-editable-error')
        elif name == 'automatic-non-editable-error':
            pass
        else:
            label.set_name('error')
            logger.log_data(
                'Unable to set name property to indicate error is "%s" for label'
                % is_error,
                widget_name)
            logger.log_data('The previous name for the label was', name)
            logger.log_data('The new name for the label is', label.get_name())
    else:
        if name == 'normal':
            pass
        elif name == 'error':
            label.set_name('normal')
            # GLib.idle_add(Gtk.Label.set_name, label, 'normal')
        elif name == 'non-editable':
            pass
        elif name == 'non-editable-error':
            label.set_name('non-editable')
            # GLib.idle_add(Gtk.Label.set_name, label, 'non-editable')
        elif name == 'automatic':
            pass
        elif name == 'automatic-error':
            label.set_name('automatic')
            # GLib.idle_add(Gtk.Label.set_name, label, 'automatic')
        elif name == 'automatic-non-editable':
            pass
        elif name == 'automatic-non-editable-error':
            label.set_name('automatic-non-editable')
            # GLib.idle_add(Gtk.Label.set_name, label, 'automatic-non-editable')
        else:
            label.set_name('normal')
            logger.log_data(
                'Unable to set name property to indicate error is "%s" for label'
                % is_error,
                widget_name)
            logger.log_data('The previous name for the label was', name)
            logger.log_data('The new name for the label is', label.get_name())
    # logger.log_data('The new name for the label is', label.get_name())


def set_entry_error(widget_name, is_error):
    # logger.log_data('Set name property to error is "%s" for entry' % is_error, widget_name)
    entry = model.builder.get_object(widget_name)
    name = entry.get_name()
    # logger.log_data('The current name for the entry is', name)
    if is_error:
        if name == 'normal':
            entry.set_name('error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'error')
        elif name == 'error':
            pass
        elif name == 'non-editable':
            entry.set_name('non-editable-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'non-editable-error')
        elif name == 'non-editable-error':
            pass
        elif name == 'automatic':
            entry.set_name('automatic-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-error')
        elif name == 'automatic-error':
            pass
        elif name == 'automatic-non-editable':
            entry.set_name('automatic-non-editable-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-non-editable-error')
        elif name == 'automatic-non-editable-error':
            pass
        else:
            entry.set_name('error')
            logger.log_data(
                'Unable to set name property to indicate error is "%s" for entry'
                % is_error,
                widget_name)
            logger.log_data('The previous name for the entry was', name)
            logger.log_data('The new name for the entry is', entry.get_name())
    else:
        if name == 'normal':
            pass
        elif name == 'error':
            entry.set_name('normal')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'normal')
        elif name == 'non-editable':
            pass
        elif name == 'non-editable-error':
            entry.set_name('non-editable')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'non-editable')
        elif name == 'automatic':
            pass
        elif name == 'automatic-error':
            entry.set_name('automatic')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic')
        elif name == 'automatic-non-editable':
            pass
        elif name == 'automatic-non-editable-error':
            entry.set_name('automatic-non-editable')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-non-editable')
        else:
            entry.set_name('normal')
            logger.log_data(
                'Unable to set name property to indicate error is "%s" for entry'
                % is_error,
                widget_name)
            logger.log_data('The previous name for the entry was', name)
            logger.log_data('The new name for the entry is', entry.get_name())
    # logger.log_data('The new name for the entry is', entry.get_name())


# TODO: Add function: set_label_editable(widget_name, is_editable)


def set_entry_editable(widget_name, is_editable):
    # logger.log_data('Set name property to editable is "%s" for entry' % is_editable, widget_name)
    entry = model.builder.get_object(widget_name)
    name = entry.get_name()
    # logger.log_data('The current name for the entry is', name)
    if is_editable:
        # logger.log_data('Set "editable" for entry', widget_name)
        if name == 'normal':
            pass
        elif name == 'error':
            pass
        elif name == 'non-editable':
            entry.set_name('normal')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'normal')
        elif name == 'non-editable-error':
            entry.set_name('error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'error')
        elif name == 'automatic':
            pass
        elif name == 'automatic-error':
            pass
        elif name == 'automatic-non-editable':
            entry.set_name('automatic')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic')
        elif name == 'automatic-non-editable-error':
            entry.set_name('automatic-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-error')
        else:
            entry.set_name('normal')
            logger.log_data(
                'Unable to set name property to indicate editable is "%s" for entry'
                % is_editable,
                widget_name)
            logger.log_data('The previous name for the entry was', name)
            logger.log_data('The new name for the entry is', entry.get_name())
    else:
        # logger.log_data('Set "non-editable" for entry', widget_name)
        if name == 'normal':
            entry.set_name('non-editable')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'non-editable')
        elif name == 'error':
            entry.set_name('non-editable-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'non-editable-error')
        elif name == 'non-editable':
            pass
        elif name == 'non-editable-error':
            pass
        elif name == 'automatic':
            entry.set_name('automatic-non-editable')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-non-editable')
        elif name == 'automatic-error':
            entry.set_name('automatic-non-editable-error')
            # GLib.idle_add(Gtk.Entry.set_name, entry,'automatic-non-editable-error')
        elif name == 'automatic-non-editable':
            pass
        elif name == 'automatic-non-editable-error':
            pass
        else:
            entry.set_name('non-editable')
            logger.log_data(
                'Unable to set name property to indicate editable is "%s" for entry'
                % is_editable,
                widget_name)
            logger.log_data('The previous name for the entry was', name)
            logger.log_data('The new name for the entry is', entry.get_name())

    entry.set_editable(is_editable)
    # logger.log_data('The new name for the entry is', entry.get_name())


def show_spinner():
    grid = model.builder.get_object('pages')
    GLib.idle_add(Gtk.Grid.set_sensitive, grid, False)

    spinner = model.builder.get_object('window_spinner')
    GLib.idle_add(Gtk.Spinner.start, spinner)
    GLib.idle_add(Gtk.Spinner.set_visible, spinner, True)


def hide_spinner():
    spinner = model.builder.get_object('window_spinner')
    GLib.idle_add(Gtk.Spinner.set_visible, spinner, False)
    GLib.idle_add(Gtk.Spinner.stop, spinner)

    grid = model.builder.get_object('pages')
    GLib.idle_add(Gtk.Grid.set_sensitive, grid, True)


def update_label(label_name, text):
    label = model.builder.get_object(label_name)
    GLib.idle_add(Gtk.Label.set_text, label, text)


def update_entry(entry_name, text):
    entry = model.builder.get_object(entry_name)
    GLib.idle_add(Gtk.Entry.set_text, entry, text)


def update_menuitem(menuitem_name, text):
    menuitem = model.builder.get_object(menuitem_name)
    GLib.idle_add(Gtk.MenuItem.set_label, menuitem, text)


def update_progressbar_percent(progressbar_name, percent):
    progressbar = model.builder.get_object(progressbar_name)
    GLib.idle_add(
        Gtk.ProgressBar.set_fraction,
        progressbar,
        float(percent) / 100.0)


def update_progressbar_text(progressbar_name, text):
    progressbar = model.builder.get_object(progressbar_name)
    GLib.idle_add(Gtk.ProgressBar.set_text, progressbar, text)


def activate_radiobutton(radiobutton_name, is_active):
    radiobutton = model.builder.get_object(radiobutton_name)
    GLib.idle_add(Gtk.RadioButton.set_active, radiobutton, is_active)


def insert_listbox_row_label(
        listbox_name,
        row_number,
        text,
        additional_height=0):
    # Since label is not displayed, there is no need to call GLib.idle_add().
    label = Gtk.Label(text)
    label.set_halign(Gtk.Align.START)
    label.set_visible(True)
    preferred_height = label.get_preferred_height()[0]
    label.set_size_request(-1, preferred_height + additional_height)

    listbox = model.builder.get_object(listbox_name)
    GLib.idle_add(Gtk.ListBox.insert, listbox, label, row_number)


def insert_listbox_row_checkbutton(
        listbox_name,
        row_number,
        text,
        is_active,
        additional_height=0):
    # Since checkbutton is not displayed, there is no need to call GLib.idle_add().
    checkbutton = Gtk.CheckButton(text)
    checkbutton.set_halign(Gtk.Align.START)
    checkbutton.set_visible(True)
    checkbutton.set_active(is_active)
    preferred_height = checkbutton.get_preferred_height()[0]
    checkbutton.set_size_request(-1, preferred_height + additional_height)

    listbox = model.builder.get_object(listbox_name)
    GLib.idle_add(Gtk.ListBox.insert, listbox, checkbutton, row_number)


def get_listbox_row_count(listbox_name):
    listbox = model.builder.get_object(listbox_name)
    return len(listbox.get_children())


def get_listbox_row_widget(listbox_name, row_number):
    listbox = model.builder.get_object(listbox_name)
    listbox_row = listbox.get_row_at_index(row_number)

    child = listbox_row.get_children()[0]

    return child


def scroll_to_tree_view_row(tree_view_name, row_number):

    tree_view = model.builder.get_object(tree_view_name)
    tree_path = Gtk.TreePath.new_from_string('%s' % row_number)
    GLib.idle_add(
        Gtk.TreeView.scroll_to_cell,
        tree_view,
        tree_path,
        None,
        True,
        0.5,
        0.0)


def select_tree_view_row(tree_view_name, row_number):

    tree_view = model.builder.get_object(tree_view_name)
    tree_path = Gtk.TreePath.new_from_string('%s' % row_number)
    GLib.idle_add(Gtk.TreeView.set_cursor, tree_view, tree_path, None, False)


# TODO: This function is not used.
def select_listbox_row(listbox_name, row_number):
    listbox = model.builder.get_object(listbox_name)
    listbox_row = listbox.get_row_at_index(row_number)

    GLib.idle_add(Gtk.ListBox.select_row, listbox, listbox_row)


def update_listbox_row_label(listbox_name, row_number, text):
    listbox = model.builder.get_object(listbox_name)
    listbox_row = listbox.get_row_at_index(row_number)
    label = listbox_row.get_children()[0]

    GLib.idle_add(Gtk.Label.set_text, label, text)


def empty_listbox(listbox_name):
    listbox = model.builder.get_object(listbox_name)
    for listbox_row in listbox.get_children():
        child = listbox_row.get_children()[0]
        if isinstance(child, Gtk.Label):
            logger.log_data('Removing label', child.get_text())
        elif isinstance(child, Gtk.Button):
            logger.log_data('Removing button', child.get_label())
        else:
            logger.log_data('Removing unknown type', child)
        GLib.idle_add(Gtk.ListBox.remove, listbox, listbox_row)
        GLib.idle_add(Gtk.Widget.destroy, listbox_row)


def update_liststore(liststore_name, data_list):
    liststore = model.builder.get_object(liststore_name)
    GLib.idle_add(_update_liststore_rows, liststore, data_list)


# This function is invoked using GLib.idle_add.
def _update_liststore_rows(liststore, data_list):
    liststore.clear()
    for number, data in enumerate(data_list):
        # logger.log_data('%i. Adding an item to the list' % (number+1), data)
        liststore.append(data)


def update_liststore_progressbar_percent(liststore_name, path, percent):
    liststore = model.builder.get_object(liststore_name)
    GLib.idle_add(
        _update_liststore_progressbar_percent,
        liststore,
        path,
        percent)


# This function is invoked using GLib.idle_add.
def _update_liststore_progressbar_percent(liststore, path, percent):
    liststore[path][0] = percent


def update_status(prefix, status):
    # The proper naming convention must be used.
    # Object ids must end in '_status' or '_spinner'.
    # Object ids ending in '_status' are always images in the *.ui file.
    # Object ids ending in '_spinner' are always spinners in the *.ui file.

    image = model.builder.get_object('%s_status' % prefix)
    GLib.idle_add(
        Gtk.Image.set_from_icon_name,
        image,
        icons[status],
        Gtk.IconSize.BUTTON)
    # GLib.idle_add(Gtk.Image.set_opacity, image, False)

    spinner = model.builder.get_object('%s_spinner' % prefix)
    if spinner:
        if status == PROCESSING:
            GLib.idle_add(Gtk.Spinner.set_visible, spinner, True)
            # GLib.idle_add(Gtk.Spinner.set_opacity, spinner, True)
            GLib.idle_add(Gtk.Spinner.start, spinner)
        else:
            GLib.idle_add(Gtk.Spinner.set_visible, spinner, False)
            # GLib.idle_add(Gtk.Spinner.set_opacity, spinner, False)
            GLib.idle_add(Gtk.Spinner.stop, spinner)


def reset_buttons(
        is_quit_visible=False,
        is_back_visible=False,
        is_next_visible=False,
        quit_button_label='Quit',
        back_button_label='Back',
        next_button_label='Next'):
    button = model.builder.get_object('quit_button')
    GLib.idle_add(Gtk.Button.set_sensitive, button, is_quit_visible)
    GLib.idle_add(Gtk.Button.set_label, button, quit_button_label)

    button = model.builder.get_object('back_button')
    GLib.idle_add(Gtk.Button.set_sensitive, button, is_back_visible)
    GLib.idle_add(Gtk.Button.set_label, button, back_button_label)

    button = model.builder.get_object('next_button')
    GLib.idle_add(Gtk.Button.set_sensitive, button, is_next_visible)
    GLib.idle_add(Gtk.Button.set_label, button, next_button_label)


def show_page(old_page_name, new_page_name):
    # Hide the current page.
    logger.log_data('Hiding old page', old_page_name)
    grid = model.builder.get_object(old_page_name)
    GLib.idle_add(Gtk.Grid.set_visible, grid, False)

    # Show the next page
    logger.log_data('Showing new page', new_page_name)
    grid = model.builder.get_object(new_page_name)
    GLib.idle_add(Gtk.Grid.set_visible, grid, True)

    # Set the current page name.
    model.set_page_name(new_page_name)

    # Allow the window to refresh, and avoid race conditions.
    time.sleep(0.25)


def add_to_stack(stack_name, filepaths, *search_replace_tuples):
    GLib.idle_add(_add_to_stack, stack_name, filepaths, *search_replace_tuples)


# This function is invoked using GLib.idle_add.
# The argument *search_replace_tuples is an optional list of tuples.
# Each tuple must contain a search_text and a replacement_text.
def _add_to_stack(stack_name, filepaths, *search_replace_tuples):

    stack = model.builder.get_object(stack_name)

    # TODO: Remove this line when 14.04 is no longer supported.
    # Bypass this functionality for Ubuntu 14.04.
    # Thsis is necessary because Gtk 3.10 in Ubuntu 14.04 does not support
    # Gtk.Stack or Gtk.StackSidebar.
    if not stack: return

    # Remove all items from the stack.
    logger.log_data('Remove all items from the stack', stack_name)
    scrolled_windows = stack.get_children()
    for scrolled_window in scrolled_windows:
        stack.remove(scrolled_window)

    # Prepate search settings.
    search_settings = GtkSource.SearchSettings()
    search_settings.set_regex_enabled(True)
    search_settings.set_wrap_around(True)

    # Add new items to the stack.
    logger.log_data('Add new items to stack', stack_name)
    for filepath in filepaths:

        title = '/%s' % os.path.relpath(
            filepath,
            model.custom_live_iso_directory)

        if os.path.exists(filepath):
            logger.log_data('Add %s from filepath' % title, filepath)

            # Create a new scrolled window.
            builder_temp = Gtk.Builder.new_from_file(timbrel_cfg.path + '/ui/scrolled_window.ui')
            scrolled_window = builder_temp.get_object('scrolled_window')

            # Get the source buffer.
            source_view = scrolled_window.get_child()
            source_buffer = source_view.get_buffer()

            # Read the file, and add it to the source buffer.
            with open(filepath, 'r') as file:
                data = file.read()
                source_buffer.set_text(data)

            # Add the new scrolled window to the stack.
            stack.add_titled(scrolled_window, filepath, title)

            # Optionally replace text.
            for search_replace_tuple in search_replace_tuples:
                search_text, replacement_text = search_replace_tuple
                logger.log_data(
                    'Search and replace',
                    '%s ⊳ %s' % (search_text,
                                 replacement_text))
                search_settings.set_search_text(search_text)
                search_context = GtkSource.SearchContext.new(
                    source_buffer,
                    search_settings)
                replacement_count = search_context.replace_all(
                    replacement_text,
                    -1)
                logger.log_data('Number of matches', replacement_count)
        else:
            logger.log_data(
                'Skip adding %s because the file does not exist' % title,
                filepath)


# This function blocks and does not use GLib.idle_add.
# The argument *search_replace_tuples is an optional list of tuples.
# Each tuple must contain a search_text and a replacement_text.
def replace_text_in_stack_buffer(stack_name, *search_replace_tuples):

    stack = model.builder.get_object(stack_name)

    # TODO: Remove this line when 14.04 is no longer supported.
    # Bypass this functionality for Ubuntu 14.04.
    # Thsis is necessary because Gtk 3.10 in Ubuntu 14.04 does not support
    # Gtk.Stack or Gtk.StackSidebar.
    if not stack: return

    logger.log_data('Searh and replace in stack', stack_name)

    # Prepate search settings.
    search_settings = GtkSource.SearchSettings()
    search_settings.set_regex_enabled(True)
    search_settings.set_wrap_around(True)

    scrolled_windows = stack.get_children()
    for scrolled_window in scrolled_windows:

        source_view = scrolled_window.get_child()
        source_buffer = source_view.get_buffer()

        total_replacement_count = 0
        for search_replace_tuple in search_replace_tuples:
            search_text, replacement_text = search_replace_tuple
            logger.log_data(
                'Search and replace',
                '%s ⊳ %s' % (search_text,
                             replacement_text))
            search_settings.set_search_text(search_text)
            search_context = GtkSource.SearchContext.new(
                source_buffer,
                search_settings)
            replacement_count = search_context.replace_all(
                replacement_text,
                -1)
            logger.log_data('Number of matches', replacement_count)
            total_replacement_count += replacement_count

    return total_replacement_count


def main_quit():
    time.sleep(0.50)
    GLib.idle_add(Gtk.main_quit)
