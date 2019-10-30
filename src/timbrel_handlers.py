#!/usr/bin/python3

########################################################################
#                                                            
# timbrel_handlers.py                                          
#                                                                   
# Copyright (C) 2019 Alexander Gribkov <https://github.com/sallecta/timbrel>             
# Copyright (C) 2015 PJ Singh <psingh.cubic@gmail.com>             
#                                                                      
########################################################################

########################################################################
#                                                                   
# This file is part of Timbrel - Custom Ubuntu ISO Creator.      
#                                                                    
# Timbrel is free software: you can redistribute it and/or modify      
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or    
# (at your option) any later version.                               
#                                                                    
# Timbrel is distributed in the hope that it will be useful,         
# but WITHOUT ANY WARRANTY; without even the implied warranty of   
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the     
# GNU General Public License for more details.                        
#                                                                    
# You should have received a copy of the GNU General Public License    
# along with Timbrel. If not, see <http://www.gnu.org/licenses/>.       
#                                                                      #
########################################################################
me='timbrel_handlers.py'
import timbrel_log

import display
import model
import transition
import utilities
import validators

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from gi.repository import Gtk
import os
import re
import time

####################################################################
# Window
####################################################################


# Do not delete on_style_updated function or:
# File "/usr/lib/python3/dist-packages/gi/overrides/Gtk.py", line 103, in _builder_connect_callback
# handler, args = _extract_handler_and_args(obj_or_map, handler_name)
# File "/usr/lib/python3/dist-packages/gi/overrides/Gtk.py", line 83, in _extract_handler_and_args
# raise AttributeError('Handler %s not found' % handler_name)
# AttributeError: Handler on_style_updated not found
def on_style_updated(window):
    pass
    # timbrel_log.info(me,'Style updated')
    # new_theme_style = display.get_theme_style(window)
    # timbrel_log.info(me,'new_theme_style',new_theme_style)
    # display.update_icon_path(new_theme_style)



####################################################################
# Password Dialog Handlers (Not Used)
####################################################################


def on_clicked__password_dialog__cancel_button(widget):

    timbrel_log.info(me,'Button clicked:', 'Password Cancel')

    display.main_quit()


def on_clicked__password_dialog__ok_button(widget):

    timbrel_log.info(me,'Button clicked:', 'Password OK')

    entry = model.builder.get_object('password_dialog__password_entry')
    password = entry.get_text()
    timbrel_log.info(me,'The password is', password)


def on_destroy__password_dialog(*args):

    timbrel_log.info(me,'Button clicked:', 'Password Dialog Delete')

    display.main_quit()


####################################################################
# Navigation Bar Handlers
####################################################################


def on_destroy(*args):

    timbrel_log.info(me,'Button clicked:', 'Window Exit')

    model.transition_thread = transition.TransitionThread(
        model.page_name,
        'exit',
        model.transition_thread)
    model.transition_thread.start()


def on_clicked__quit_button(widget):

    timbrel_log.info(me,'Button clicked:', 'Quit')

    model.transition_thread = transition.TransitionThread(
        model.page_name,
        'exit',
        model.transition_thread)
    model.transition_thread.start()


def on_clicked__next_button(widget):

    # Project Directory Page
    # New Project Page
    # Existing Project Page
    # Delete Project Page
    # Unsquashfs Page
    # Terminal Page
    # Copy Files Page
    # Options Page
    # Repackage ISO Page
    # Finish Page

    timbrel_log.info(me,'Button clicked:', 'Next')

    new_page_name = None

    if model.page_name == 'project_directory_page':
        if not os.path.exists(model.configuration_filepath):
            new_page_name = 'new_project_page'
        else:
            new_page_name = 'existing_project_page'
    elif model.page_name == 'new_project_page':
        new_page_name = 'terminal_page'
    elif model.page_name == 'existing_project_page':
        if model.builder.get_object(
                'existing_project_page__radiobutton_1').get_active():
            new_page_name = 'options_page'
        elif model.builder.get_object(
                'existing_project_page__radiobutton_2').get_active():
            new_page_name = 'terminal_page'
        elif model.builder.get_object(
                'existing_project_page__radiobutton_3').get_active():
            new_page_name = 'delete_project_page'
    elif model.page_name == 'delete_project_page':
        new_page_name = 'new_project_page'
    elif model.page_name == 'unsquashfs_page':
        new_page_name = 'terminal_page'
    elif model.page_name == 'terminal_page':
        new_page_name = 'options_page'
    elif model.page_name == 'copy_files_page':
        new_page_name = 'terminal_page_copy_files'
    elif model.page_name == 'options_page':
        new_page_name = 'repackage_iso_page'
    elif model.page_name == 'repackage_iso_page':
        new_page_name = 'finish_page'
    elif model.page_name == 'finish_page':
        new_page_name = 'exit'
    else:
        timbrel_log.error(me,'Next page for the current page is not defined', model.page_name)

    model.transition_thread = transition.TransitionThread(
        model.page_name,
        new_page_name)
    model.transition_thread.start()


def on_clicked__back_button(widget):

    # Project Directory Page
    # New Project Page
    # Existing Project Page
    # Delete Project Page
    # Unsquashfs Page
    # Terminal Page
    # Copy Files Page
    # Options Page
    # Repackage ISO Page
    # Finish Page

    timbrel_log.info(me,'Button clicked:', 'Back')

    new_page_name = None

    if model.page_name == 'project_directory_page':
        pass
    elif model.page_name == 'new_project_page':
        new_page_name = 'project_directory_page'
    elif model.page_name == 'existing_project_page':
        new_page_name = 'project_directory_page'
    elif model.page_name == 'delete_project_page':
        new_page_name = 'existing_project_page'
    elif model.page_name == 'unsquashfs_page':
        new_page_name = 'existing_project_page'
    elif model.page_name == 'terminal_page':
        new_page_name = 'existing_project_page'
    elif model.page_name == 'copy_files_page':
        new_page_name = 'terminal_page_cancel_copy_files'
    elif model.page_name == 'options_page':
        if model.builder.get_object(
                'existing_project_page__radiobutton_1').get_active():
            # - Radio button 1 (create a disk image from the existing project)
            # - was selected on the Existing Project page.
            new_page_name = 'existing_project_page'
        elif model.builder.get_object(
                'existing_project_page__radiobutton_2').get_active():
            # - Radio button 2 (continue customizing the existing project).
            #   was programmatically set in the function
            #   transition__from__project_directory_page__to__new_project_page()
            # Case for an existing project:
            # - Radio button 2 (create a disk image from the existing project)
            # - was selected on the Existing Project page.
            new_page_name = 'terminal_page'
        else:
            timbrel_log.error(me,'Back page for the current page is not defined', model.page_name)
    elif model.page_name == 'repackage_iso_page':
        new_page_name = 'options_page'
    else:
        # Error
        timbrel_log.error(me,'Error. Back page for the current page is not defined',model.page_name)

    model.transition_thread = transition.TransitionThread(
        model.page_name,
        new_page_name,
        model.transition_thread)
    model.transition_thread.start()


####################################################################
# Project Directory Page Handlers
####################################################################


def on_clicked__project_directory_page__project_directory_filechooser__open_button(
        widget):

    os.setegid(model.group_id)
    os.seteuid(model.user_id)

    display.set_sensitive('window', False)

    dialog = model.builder.get_object(
        'project_directory_page__project_directory_filechooser')
    dialog.set_current_folder(model.home)

    dialog.show_all()


def on_changed__project_directory_page__project_directory_entry(widget):

    model.set_project_directory(widget.get_text())

    model.set_configuration_filepath(
        utilities.create_configuration_filepath(model.project_directory))
    model.set_original_iso_image_mount_point(
        utilities.create_original_iso_image_mount_point(
            model.project_directory))
    model.set_custom_squashfs_directory(
        utilities.create_custom_squashfs_directory(model.project_directory))
    model.set_custom_live_iso_directory(
        utilities.create_custom_live_iso_directory(model.project_directory))

    validators.validate_project_directory_page()


####################################################################
# Project Directory Page Filechooser Handlers
####################################################################


def on_delete_event__project_directory_page__project_directory_filechooser(
        widget,
        event):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    # Synchronously invoke hide_on_delete() because this function must return
    # True only when hide_on_delete() completes.
    # display.hide_on_delete('project_directory_page__project_directory_filechooser')
    widget.hide_on_delete()

    display.set_sensitive('window', True)

    return True


def on_clicked__project_directory_page__project_directory_filechooser__cancel_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('project_directory_page__project_directory_filechooser')

    display.set_sensitive('window', True)


def on_clicked__project_directory_page__project_directory_filechooser__select_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('project_directory_page__project_directory_filechooser')

    model.transition_thread = transition.TransitionThread(
        'project_directory_page__project_directory_filechooser',
        'project_directory_page',
        model.transition_thread)
    model.transition_thread.start()

    # display.set_sensitive('window', True)


####################################################################
# New Project Page Handlers - Original ISO
####################################################################


def on_clicked__new_project_page__original_iso_image_filepath_filechooser__open_button(
        widget):

    os.setegid(model.group_id)
    os.seteuid(model.user_id)

    display.set_sensitive('window', False)

    dialog = model.builder.get_object(
        'new_project_page__original_iso_image_filepath_filechooser')
    if os.path.exists(model.original_iso_image_filepath):
        dialog.set_filename(model.original_iso_image_filepath)
    elif os.path.exists(model.original_iso_image_directory):
        dialog.set_current_folder(model.original_iso_image_directory)
    else:
        dialog.set_current_folder(model.home)

    dialog.show_all()


####################################################################
# New Project Page Handlers - Custom ISO
####################################################################


def on_clicked__new_project_page__custom_iso_image_directory_filechooser__open_button(
        widget):

    os.setegid(model.group_id)
    os.seteuid(model.user_id)

    display.set_sensitive('window', False)

    dialog = model.builder.get_object(
        'new_project_page__custom_iso_image_directory_filechooser')
    if os.path.exists(model.custom_iso_image_directory):
        dialog.set_current_folder(model.custom_iso_image_directory)
    else:
        dialog.set_current_folder(model.home)

    dialog.show_all()


def on_changed__new_project_page__custom_iso_image_version_number_entry(
        widget):

    model.set_custom_iso_image_version_number(widget.get_text())

    if model.propagate:
        custom_iso_image_filename = utilities.create_custom_iso_image_filename(
            model.original_iso_image_filename,
            model.custom_iso_image_version_number)
        display.update_entry(
            'new_project_page__custom_iso_image_filename_entry',
            custom_iso_image_filename)

        custom_iso_image_volume_id = utilities.create_custom_iso_image_volume_id(
            model.original_iso_image_volume_id,
            model.custom_iso_image_version_number)
        display.update_entry(
            'new_project_page__custom_iso_image_volume_id_entry',
            custom_iso_image_volume_id)

    validators.validate_new_project_page_custom()


def on_changed__new_project_page__custom_iso_image_filename_entry(widget):

    text = widget.get_text()
    if text:
        if text[-8:] == '.iso.iso':
            position = widget.get_property('cursor-position')
            widget.set_text(text[:-4])
            widget.set_position(position)
        elif text[-4:] != '.iso':
            position = widget.get_property('cursor-position')
            widget.set_text(text + '.iso')
            widget.set_position(position)

    model.set_custom_iso_image_filename(widget.get_text())
    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))

    model.set_custom_iso_image_md5_filename(
        utilities.create_custom_iso_image_md5_filename(
            model.custom_iso_image_filename))
    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    validators.validate_new_project_page_custom()


def on_changed__new_project_page__custom_iso_image_directory_entry(widget):

    model.set_custom_iso_image_directory(widget.get_text())

    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))

    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    validators.validate_new_project_page_custom()


def on_changed__new_project_page__custom_iso_image_volume_id_entry(widget):

    model.set_custom_iso_image_volume_id(widget.get_text())

    if model.propagate:
        custom_iso_image_disk_name = utilities.create_custom_iso_image_disk_name(
            model.custom_iso_image_volume_id,
            model.custom_iso_image_release_name)
        display.update_entry(
            'new_project_page__custom_iso_image_disk_name_entry',
            custom_iso_image_disk_name)

    validators.validate_new_project_page_custom()


def on_changed__new_project_page__custom_iso_image_release_name_entry(widget):

    model.set_custom_iso_image_release_name(widget.get_text())

    if model.propagate:
        custom_iso_image_disk_name = utilities.create_custom_iso_image_disk_name(
            model.custom_iso_image_volume_id,
            model.custom_iso_image_release_name)
        display.update_entry(
            'new_project_page__custom_iso_image_disk_name_entry',
            custom_iso_image_disk_name)

    validators.validate_new_project_page_custom()


def on_changed__new_project_page__custom_iso_image_disk_name_entry(widget):

    model.set_custom_iso_image_disk_name(widget.get_text())

    validators.validate_new_project_page_custom()


####################################################################
# New Project Page Filechooser Handlers
####################################################################


def on_delete_event__new_project_page__original_iso_image_filepath_filechooser(
        widget,
        event):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    # Synchronously invoke hide_on_delete() because this function must return
    # True only when hide_on_delete() completes.
    # display.hide_on_delete('new_project_page__original_iso_image_filepath_filechooser')
    widget.hide_on_delete()

    display.set_sensitive('window', True)

    return True


def on_clicked__new_project_page__original_iso_image_filepath_filechooser__cancel_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('new_project_page__original_iso_image_filepath_filechooser')

    display.set_sensitive('window', True)


def on_clicked__new_project_page__original_iso_image_filepath_filechooser__select_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('new_project_page__original_iso_image_filepath_filechooser')

    model.transition_thread = transition.TransitionThread(
        'original_iso_image_filepath_filechooser',
        'new_project_page',
        model.transition_thread)
    model.transition_thread.start()

    # display.set_sensitive('window', True)


def on_delete_event__new_project_page__custom_iso_image_directory_filechooser(
        widget,
        event):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    # Synchronously invoke hide_on_delete() because this function must return
    # True only when hide_on_delete() completes.
    # display.hide_on_delete('new_project_page__custom_iso_image_directory_filechooser')
    widget.hide_on_delete()

    display.set_sensitive('window', True)

    return True


def on_clicked__new_project_page__custom_iso_image_directory_filechooser__cancel_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('new_project_page__custom_iso_image_directory_filechooser')

    display.set_sensitive('window', True)


def on_clicked__new_project_page__custom_iso_image_directory_filechooser__select_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide('new_project_page__custom_iso_image_directory_filechooser')

    model.transition_thread = transition.TransitionThread(
        'custom_iso_image_directory_filechooser',
        'new_project_page',
        model.transition_thread)
    model.transition_thread.start()

    # display.set_sensitive('window', True)


####################################################################
# Existing Project Page Handlers - Radio Buttons
####################################################################


def on_toggled__existing_project_page__radiobutton(widget):

    # Prevent propogatoin if we are changing the state of the radiobutton
    # group programmatically.
    if model.propagate:
        model.transition_thread = transition.TransitionThread(
            'existing_project_page',
            'existing_project_page',
            model.transition_thread)
        model.transition_thread.start()


####################################################################
# Existing Project Page Handlers - Original ISO
####################################################################


def on_clicked__existing_project_page__original_iso_image_filepath_filechooser__open_button(
        widget):

    os.setegid(model.group_id)
    os.seteuid(model.user_id)

    display.set_sensitive('window', False)

    dialog = model.builder.get_object(
        'existing_project_page__original_iso_image_filepath_filechooser')
    if os.path.exists(model.original_iso_image_filepath):
        dialog.set_filename(model.original_iso_image_filepath)
    elif os.path.exists(model.original_iso_image_directory):
        dialog.set_current_folder(model.original_iso_image_directory)
    else:
        dialog.set_current_folder(model.home)

    dialog.show_all()


####################################################################
# Existing Project Page Handlers - Custom ISO
####################################################################


def on_clicked__existing_project_page__custom_iso_image_directory_filechooser__open_button(
        widget):

    os.setegid(model.group_id)
    os.seteuid(model.user_id)

    display.set_sensitive('window', False)

    dialog = model.builder.get_object(
        'existing_project_page__custom_iso_image_directory_filechooser')
    if os.path.exists(model.custom_iso_image_directory):
        dialog.set_current_folder(model.custom_iso_image_directory)
    else:
        dialog.set_current_folder(model.home)

    dialog.show_all()


def on_changed__existing_project_page__custom_iso_image_version_number_entry(
        widget):

    model.set_custom_iso_image_version_number(widget.get_text())

    if model.propagate:
        custom_iso_image_filename = utilities.create_custom_iso_image_filename(
            model.original_iso_image_filename,
            model.custom_iso_image_version_number)
        display.update_entry(
            'existing_project_page__custom_iso_image_filename_entry',
            custom_iso_image_filename)

        custom_iso_image_volume_id = utilities.create_custom_iso_image_volume_id(
            model.original_iso_image_volume_id,
            model.custom_iso_image_version_number)
        display.update_entry(
            'existing_project_page__custom_iso_image_volume_id_entry',
            custom_iso_image_volume_id)

    validators.validate_existing_project_page_custom()


def on_changed__existing_project_page__custom_iso_image_filename_entry(widget):

    text = widget.get_text()
    if text:
        if text[-8:] == '.iso.iso':
            position = widget.get_property('cursor-position')
            widget.set_text(text[:-4])
            widget.set_position(position)
        elif text[-4:] != '.iso':
            position = widget.get_property('cursor-position')
            widget.set_text(text + '.iso')
            widget.set_position(position)

    model.set_custom_iso_image_filename(widget.get_text())
    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))

    model.set_custom_iso_image_md5_filename(
        utilities.create_custom_iso_image_md5_filename(
            model.custom_iso_image_filename))
    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    validators.validate_existing_project_page_custom()


def on_changed__existing_project_page__custom_iso_image_directory_entry(
        widget):

    model.set_custom_iso_image_directory(widget.get_text())

    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))

    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    validators.validate_existing_project_page_custom()


def on_changed__existing_project_page__custom_iso_image_volume_id_entry(
        widget):

    model.set_custom_iso_image_volume_id(widget.get_text())

    if model.propagate:
        custom_iso_image_disk_name = utilities.create_custom_iso_image_disk_name(
            model.custom_iso_image_volume_id,
            model.custom_iso_image_release_name)
        display.update_entry(
            'existing_project_page__custom_iso_image_disk_name_entry',
            custom_iso_image_disk_name)

    validators.validate_existing_project_page_custom()


def on_changed__existing_project_page__custom_iso_image_release_name_entry(
        widget):

    model.set_custom_iso_image_release_name(widget.get_text())

    if model.propagate:
        custom_iso_image_disk_name = utilities.create_custom_iso_image_disk_name(
            model.custom_iso_image_volume_id,
            model.custom_iso_image_release_name)
        display.update_entry(
            'existing_project_page__custom_iso_image_disk_name_entry',
            custom_iso_image_disk_name)

    validators.validate_existing_project_page_custom()


def on_changed__existing_project_page__custom_iso_image_disk_name_entry(
        widget):

    model.set_custom_iso_image_disk_name(widget.get_text())

    validators.validate_existing_project_page_custom()


####################################################################
# Existing Project Page Filechooser Handlers
####################################################################


def on_delete_event__existing_project_page__original_iso_image_filepath_filechooser(
        widget,
        event):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    # Synchronously invoke hide_on_delete() because this function must return
    # True only when hide_on_delete() completes.
    # display.hide_on_delete('existing_project_page__original_iso_image_filepath_filechooser')
    widget.hide_on_delete()

    display.set_sensitive('window', True)

    return True


def on_clicked__existing_project_page__original_iso_image_filepath_filechooser__cancel_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide(
        'existing_project_page__original_iso_image_filepath_filechooser')

    display.set_sensitive('window', True)


def on_clicked__existing_project_page__original_iso_image_filepath_filechooser__select_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide(
        'existing_project_page__original_iso_image_filepath_filechooser')

    model.transition_thread = transition.TransitionThread(
        'original_iso_image_filepath_filechooser',
        'existing_project_page',
        model.transition_thread)
    model.transition_thread.start()

    # display.set_sensitive('window', True)


def on_delete_event__existing_project_page__custom_iso_image_directory_filechooser(
        widget,
        event):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    # Synchronously invoke hide_on_delete() because this function must return
    # True only when hide_on_delete() completes.
    # display.hide_on_delete('existing_project_page__custom_iso_image_directory_filechooser')
    widget.hide_on_delete()

    display.set_sensitive('window', True)

    return True


def on_clicked__existing_project_page__custom_iso_image_directory_filechooser__cancel_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide(
        'existing_project_page__custom_iso_image_directory_filechooser')

    display.set_sensitive('window', True)


def on_clicked__existing_project_page__custom_iso_image_directory_filechooser__select_button(
        widget):

    os.setegid(model.root_group_id)
    os.seteuid(model.root_user_id)

    display.hide(
        'existing_project_page__custom_iso_image_directory_filechooser')

    model.transition_thread = transition.TransitionThread(
        'custom_iso_image_directory_filechooser',
        'existing_project_page',
        model.transition_thread)
    model.transition_thread.start()

    # display.set_sensitive('window', True)


####################################################################
# Confirm Delete Page Handlers - Nautilus
####################################################################


def on_clicked__delete_project_page__custom_iso_image_directory_open_button(
        widget):

    # os.startfile(custom_iso_image_directory)
    # subprocess.Popen(['xdg-open', model.custom_iso_image_directory])
    # process = subprocess.Popen(['xdg-open', model.custom_iso_image_directory], preexec_fn=utilities.set_user_and_group(model.user_id, model.group_id))
    # subprocess.call(['xdg-open', model.custom_iso_image_directory])
    # timbrel_log.info(me,'The user, group for the current process is', 'User %s, Group %s' % (os.getuid(), os.getgid()))
    return


def on_clicked__delete_project_page__custom_iso_image_md5_directory_open_button(
        widget):

    # os.startfile(custom_iso_image_directory)
    # subprocess.Popen(['xdg-open', model.custom_iso_image_directory])
    # process = subprocess.Popen(['xdg-open', model.custom_iso_image_directory], preexec_fn=utilities.set_user_and_group(model.user_id, model.group_id))
    # subprocess.call(['xdg-open', model.custom_iso_image_directory])
    # timbrel_log.info(me,'The user, group for the current process is', 'User %s, Group %s' % (os.getuid(), os.getgid()))
    return


####################################################################
# Terminal Page Handlers
####################################################################


def on_child_exited__terminal_page(*args):

    timbrel_log.info(me,'Terminal', 'exited')

    # TODO: When the user clicks the Next button on the terminal page, the
    #       chroot environment exits. Consequently the terminal exits,
    #       invoking this function. This function eventaully causes function
    #       transition__from__terminal_page__to__terminal_page to execute.
    #       However, only the function
    #       transition__from__terminal_page__to__options_page__linux_kernels_tab
    #       should be invoked.

    new_page_name = 'terminal_page'
    model.transition_thread = transition.TransitionThread(
        model.page_name,
        new_page_name)
    model.transition_thread.start()


def on_drag_data_received__terminal_page(
        widget,
        drag_context,
        x,
        y,
        data,
        info,
        drag_time):

    timbrel_log.info(me,'Drag data received for', 'terminal_page')

    # Gtk.SelectionData
    # https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/SelectionData.html

    # The data type is....................... text/uri-list
    # The data type is....................... text/plain
    atom = data.get_data_type()
    data_type = str(atom)
    timbrel_log.info(me,'The data type is', data_type)

    text = data.get_text()

    if text is not None:
        utilities.send_text_to_terminal(text)
    else:
        model.set_uris(data.get_uris())
        # Go to the next page.
        model.transition_thread = transition.TransitionThread(
            model.page_name,
            'copy_files_page')
        model.transition_thread.start()


def on_button_press_event__terminal_page(widget, event):

    if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:

        timbrel_log.info(me,'Mouse button 3 pressed for', 'terminal_page')

        terminal = model.builder.get_object('terminal_page__terminal')
        terminal_has_selection = terminal.get_has_selection()

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # Menuitem 1
        display.set_sensitive('terminal_page__select_all_menuitem', True)

        # Menuitem 2
        display.set_sensitive(
            'terminal_page__copy_text_menuitem',
            terminal_has_selection)

        # Menuitem 3
        clipboard_has_text = clipboard.wait_is_text_available()
        display.set_sensitive(
            'terminal_page__paste_text_menuitem',
            clipboard_has_text and not terminal_has_selection)

        # Menuitem 4
        clipboard_has_uris = clipboard.wait_is_uris_available()
        if clipboard_has_uris and not terminal_has_selection:
            count = len(clipboard.wait_for_uris())
            label = 'Paste File' if count == 1 else 'Paste %s Files' % count
            display.update_menuitem(
                'terminal_page__paste_file_menuitem',
                label)
            display.set_sensitive('terminal_page__paste_file_menuitem', True)
        else:
            label = 'Paste File(s)'
            display.update_menuitem(
                'terminal_page__paste_file_menuitem',
                label)
            display.set_sensitive('terminal_page__paste_file_menuitem', False)

        menu = model.builder.get_object('terminal_page__menu')
        menu.popup(None, None, None, None, event.button, event.time)


####################################################################
# Terminal Page Handlers - Popup Menu
####################################################################


def handler_button_release_event__terminal_page__select_all_menuitem(*args):

    terminal = model.builder.get_object('terminal_page__terminal')
    terminal.select_all()


def on_button_release_event__terminal_page__copy_text_menuitem(*args):

    terminal = model.builder.get_object('terminal_page__terminal')
    terminal.copy_clipboard()

    # https://lazka.github.io/pgi-docs/#Vte-2.90/classes/Terminal.html
    # https://lazka.github.io/pgi-docs/#Vte-2.91/classes/Terminal.html
    try:
        terminal.unselect_all
    except AttributeError:
        # Vte 2.90 only...
        # Ubuntu 14.04 uses libvte-2.90
        terminal.select_none()
    else:
        # Vte 2.91 only...
        # Ubuntu 15.04 uses libvte-2.91
        terminal.unselect_all()


def on_button_release_event__terminal_page__paste_text_menuitem(*args):

    terminal = model.builder.get_object('terminal_page__terminal')
    terminal.paste_clipboard()


def on_button_release_event__terminal_page__paste_file_menuitem(*args):

    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    model.set_uris(clipboard.wait_for_uris())

    # Go to the next page.

    model.transition_thread = transition.TransitionThread(
        model.page_name,
        'copy_files_page')
    model.transition_thread.start()


####################################################################
# Options Page Handlers - Kernels
####################################################################


### TODO: Conisder using a function in transitions.py for this.
###       We automatically get the spinner while the files are updated.
###       Use display.py and GLib.add_idle()
def on_toggled__options_page__linux_kernels_tab__radiobutton(widget, row):

    selected_index = int(row)
    timbrel_log.info(me,'The selected kernel is item number', selected_index)

    # 0: version_name
    # 1: vmlinuz_filename
    # 2: new_vmlinuz_filename
    # 3: initrd_filename
    # 4: new_initrd_filename
    # 5: directory
    # 6: note
    # 7: is_selected
    # 8: is_remove
    liststore = model.builder.get_object(
        'options_page__linux_kernels_tab__liststore')

    # Select clicked row, and unselect other rows.
    for number, item in enumerate(liststore):
        liststore[number][7] = (number == selected_index)

    # Search and replace text.
    stack_name = 'options_page__boot_configuration_tab__stack'
    search_text_1 = r'/vmlinuz\S*'
    replacement_text_1 = '/%s' % liststore[selected_index][2]
    search_text_2 = r'/initrd\S*'
    replacement_text_2 = '/%s' % liststore[selected_index][4]
    display.replace_text_in_stack_buffer(
        stack_name,
        (search_text_1,
         replacement_text_1),
        (search_text_2,
         replacement_text_2))


####################################################################
# Options Page Handlers - Package Manifest
####################################################################


def on_toggled__options_page__package_manifest_tab__remove_1_checkbutton(
        widget,
        row):

    # print('\nCOLUMN 0...')

    liststore = model.builder.get_object(
        'options_page__package_manifest_tab__liststore')

    column = 0
    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))

    liststore[row][0] = not liststore[row][0]

    # Even though the minimal checkbutton column may not be visible (if
    # 'filesystem.manifest-minimal-remove' does not exist, still update
    # the liststore. It's a little inefficient, but does no harm.
    if liststore[row][0]:
        # Backup original minimal checkbutton value
        liststore[row][2] = liststore[row][1]
        # Set minimal checkbutton selected
        liststore[row][1] = True
        # Set minimal checkbutton inactive
        liststore[row][3] = False
    else:
        # Restore original minimal checkbutton value
        liststore[row][1] = liststore[row][2]
        # Set minimal checkbutton active
        liststore[row][3] = True

    if len(model.undo_list) > model.undo_index:
        # print(' - Insert at %s, value %s' % (model.undo_index, [row, 0]))
        model.undo_list[model.undo_index] = [row, 0]
    else:
        # print(
        #     ' - Append at %s, value %s' % (model.undo_index + 1,
        #                                    [row,
        #                                     0]))
        model.undo_list.append([row, 0])

    model.undo_index += 1

    display.set_sensitive(
        'options_page__package_manifest_tab__revert_button',
        True)
    display.set_sensitive(
        'options_page__package_manifest_tab__undo_button',
        True)
    display.set_sensitive(
        'options_page__package_manifest_tab__redo_button',
        False)
    del model.undo_list[model.undo_index:]

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))


def on_toggled__options_page__package_manifest_tab__remove_2_checkbutton(
        widget,
        row):

    # print('\nCOLUMN 1...')

    liststore = model.builder.get_object(
        'options_page__package_manifest_tab__liststore')

    column = 1
    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))

    liststore[row][1] = not liststore[row][1]

    if len(model.undo_list) > model.undo_index:
        # print(' - Insert at %s, value %s' % (model.undo_index, [row, 1]))
        model.undo_list[model.undo_index] = [row, 1]
    else:
        # print(
        #     ' - Append at %s, value %s' % (model.undo_index + 1,
        #                                    [row,
        #                                     1]))
        model.undo_list.append([row, 1])

    model.undo_index += 1

    display.set_sensitive(
        'options_page__package_manifest_tab__revert_button',
        True)
    display.set_sensitive(
        'options_page__package_manifest_tab__undo_button',
        True)
    display.set_sensitive(
        'options_page__package_manifest_tab__redo_button',
        False)
    del model.undo_list[model.undo_index:]

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))


def on_clicked__options_page__package_manifest_tab__revert_button(widget):

    # print('\nREVERT...')

    liststore = model.builder.get_object(
        'options_page__package_manifest_tab__liststore')

    while model.undo_index > 0:

        model.undo_index -= 1

        row, column = model.undo_list[model.undo_index]

        display.select_tree_view_row(
            'options_page__package_manifest_tab__treeview',
            row)
        # display.scroll_to_tree_view_row('options_page__package_manifest_tab__treeview', row)
        # time.sleep(0.25)

        # print(
        #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
        #     % (
        #         row,
        #         column,
        #         liststore[row][0],
        #         liststore[row][1],
        #         liststore[row][2],
        #         liststore[row][3],
        #         len(model.undo_list),
        #         model.undo_index))

        if column == 0:
            liststore[row][0] = not liststore[row][0]
            # Even though the minimal checkbutton column may not be visible (if
            # 'filesystem.manifest-minimal-remove' does not exist, still update
            # the liststore. It's a little inefficient, but does no harm.
            if liststore[row][0]:
                # Backup original minimal checkbutton value
                liststore[row][2] = liststore[row][1]
                # Set minimal checkbutton selected
                liststore[row][1] = True
                # Set minimal checkbutton inactive
                liststore[row][3] = False
            else:
                # Restore original minimal checkbutton value
                liststore[row][1] = liststore[row][2]
                # Set minimal checkbutton active
                liststore[row][3] = True
        else:
            liststore[row][1] = not liststore[row][1]

    # if model.undo_index == 0:
    display.set_sensitive(
        'options_page__package_manifest_tab__revert_button',
        False)
    display.set_sensitive(
        'options_page__package_manifest_tab__undo_button',
        False)

    display.set_sensitive(
        'options_page__package_manifest_tab__redo_button',
        True)

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))


def on_clicked__options_page__package_manifest_tab__undo_button(widget):

    # print('\nUNDO...')

    model.undo_index -= 1

    liststore = model.builder.get_object(
        'options_page__package_manifest_tab__liststore')

    row, column = model.undo_list[model.undo_index]

    display.select_tree_view_row(
        'options_page__package_manifest_tab__treeview',
        row)
    # display.scroll_to_tree_view_row('options_page__package_manifest_tab__treeview', row)
    # time.sleep(0.25)

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))

    if column == 0:
        liststore[row][0] = not liststore[row][0]
        # Even though the minimal checkbutton column may not be visible (if
        # 'filesystem.manifest-minimal-remove' does not exist, still update
        # the liststore. It's a little inefficient, but does no harm.
        if liststore[row][0]:
            # Backup original minimal checkbutton value
            liststore[row][2] = liststore[row][1]
            # Set minimal checkbutton selected
            liststore[row][1] = True
            # Set minimal checkbutton inactive
            liststore[row][3] = False
        else:
            # Restore original minimal checkbutton value
            liststore[row][1] = liststore[row][2]
            # Set minimal checkbutton active
            liststore[row][3] = True
    else:
        liststore[row][1] = not liststore[row][1]

    if model.undo_index == 0:
        display.set_sensitive(
            'options_page__package_manifest_tab__revert_button',
            False)
        display.set_sensitive(
            'options_page__package_manifest_tab__undo_button',
            False)

    display.set_sensitive(
        'options_page__package_manifest_tab__redo_button',
        True)

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))


def on_clicked__options_page__package_manifest_tab__redo_button(widget):

    # print('\nREDO...')

    liststore = model.builder.get_object(
        'options_page__package_manifest_tab__liststore')

    row, column = model.undo_list[model.undo_index]

    display.select_tree_view_row(
        'options_page__package_manifest_tab__treeview',
        row)
    # display.scroll_to_tree_view_row('options_page__package_manifest_tab__treeview', row)
    # time.sleep(0.25)

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))

    if column == 0:
        liststore[row][0] = not liststore[row][0]
        # Even though the minimal checkbutton column may not be visible (if
        # 'filesystem.manifest-minimal-remove' does not exist, still update
        # the liststore. It's a little inefficient, but does no harm.
        if liststore[row][0]:
            # Backup original minimal checkbutton value
            liststore[row][2] = liststore[row][1]
            # Set minimal checkbutton selected
            liststore[row][1] = True
            # Set minimal checkbutton inactive
            liststore[row][3] = False
        else:
            # Restore original minimal checkbutton value
            liststore[row][1] = liststore[row][2]
            # Set minimal checkbutton active
            liststore[row][3] = True
    else:
        liststore[row][1] = not liststore[row][1]

    model.undo_index += 1

    if len(model.undo_list) == model.undo_index:
        display.set_sensitive(
            'options_page__package_manifest_tab__redo_button',
            False)

    display.set_sensitive(
        'options_page__package_manifest_tab__revert_button',
        True)
    display.set_sensitive(
        'options_page__package_manifest_tab__undo_button',
        True)

    # print(
    #     ' - Row: %s, Column: %s, Typical: %s, Minimal: %s, Previous: %s, Active: %s, Length: %s, Index: %s'
    #     % (
    #         row,
    #         column,
    #         liststore[row][0],
    #         liststore[row][1],
    #         liststore[row][2],
    #         liststore[row][3],
    #         len(model.undo_list),
    #         model.undo_index))


####################################################################
# Options Page Handlers - Preseed
####################################################################


def on_clicked__options_page__preseed_tab__stack_sidebar__create_button(
        widget):

    # Stack create button
    display.set_sensitive(
        'options_page__preseed_tab__stack_sidebar__create_button',
        False)

    # Stack delete button
    stack = model.builder.get_object('options_page__preseed_tab__stack')
    scrolled_window = stack.get_visible_child()
    ### scrolled_windows = stack.get_children()
    if scrolled_window:
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            True)
    else:
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            False)

    # Stack
    display.set_visible('options_page__preseed_tab__stack', False)

    # Create box
    display.update_entry('options_page__preseed_tab__create_grid__entry', '')
    display.update_label(
        'options_page__preseed_tab__create_grid__error_label',
        '')
    display.set_visible('options_page__preseed_tab__create_grid', True)

    # Delete box
    # display.update_entry('options_page__preseed_tab__delete_grid__entry', title)
    # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
    display.set_visible('options_page__preseed_tab__delete_grid', False)


def on_clicked__options_page__preseed_tab__create_grid__button(widget):

    # Get new item name.
    entry = model.builder.get_object(
        'options_page__preseed_tab__create_grid__entry')
    filename = entry.get_text()

    # Validate filename.
    pattern = r'[a-zA-Z0-9][a-zA-Z0-9\.-_]*[a-zA-Z0-9]'
    match = re.fullmatch(pattern, filename)

    if match:

        # New filename is valid.

        stack_name = 'options_page__preseed_tab__stack'
        stack = model.builder.get_object(stack_name)
        custom_live_iso_directory = os.path.realpath(
            model.custom_live_iso_directory)
        filepath = os.path.join(custom_live_iso_directory, 'preseed', filename)

        scrolled_window = stack.get_child_by_name(filepath)
        if scrolled_window:

            # Item already exists in the stack.

            timbrel_log.info(me,'Item already exists in the stack', stack_name)
            title = stack.child_get_property(scrolled_window, 'title')
            timbrel_log.info(me,'Item already in the stack')
            timbrel_log.info(me,'The title is', title)
            timbrel_log.info(me,'The name (filepath) is', filepath)
            label = model.builder.get_object(
                'options_page__preseed_tab__create_grid__error_label')
            label.set_text('Error. A file with this name already exists.')

        else:

            # Add a new item to the stack.

            timbrel_log.info(me,'Add a new item to stack', stack_name)
            title = '/%s' % os.path.join('preseed', filename)
            timbrel_log.info(me,'The title is', title)
            timbrel_log.info(me,'The name (filepath) is', filepath)

            # Create a new scrolled window.
            builder_temp = Gtk.Builder.new_from_file('scrolled_window.ui')
            scrolled_window = builder_temp.get_object('scrolled_window')

            # Ensure the file is not flaged for deletion.
            if filepath in model.delete_list:
                model.delete_list.remove(filepath)

            # Add the new scrolled window to the stack.
            stack.add_titled(scrolled_window, filepath, title)
            stack.set_visible_child(scrolled_window)

            # Show or hide widgets, as necessary.

            # Stack create button
            display.set_sensitive(
                'options_page__preseed_tab__stack_sidebar__create_button',
                True)

            # Stack delete button
            display.set_sensitive(
                'options_page__preseed_tab__stack_sidebar__delete_button',
                True)

            # Stack
            display.set_visible('options_page__preseed_tab__stack', True)

            # Create box
            # display.update_entry('options_page__preseed_tab__create_grid__entry', '')
            # display.update_label('options_page__preseed_tab__create_grid__error_label', '')
            display.set_visible(
                'options_page__preseed_tab__create_grid',
                False)

            # Delete box
            # display.update_entry('options_page__preseed_tab__delete_grid__entry', '')
            # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
            display.set_visible(
                'options_page__preseed_tab__delete_grid',
                False)

    else:

        # New filename is not valid.

        label = model.builder.get_object(
            'options_page__preseed_tab__create_grid__error_label')
        label.set_text(
            'Error. Invalid file name. Valid file names contain alpha-numeric characters, dashes, underscores, or periods.'
        )


def on_clicked__options_page__preseed_tab__stack_sidebar__delete_button(
        widget):

    # Stack create button
    display.set_sensitive(
        'options_page__preseed_tab__stack_sidebar__create_button',
        True)

    # Stack delete button
    display.set_sensitive(
        'options_page__preseed_tab__stack_sidebar__delete_button',
        False)

    # Stack
    display.set_visible('options_page__preseed_tab__stack', False)

    # Create box
    # display.update_entry('options_page__preseed_tab__create_grid__entry', '')
    # display.update_label('options_page__preseed_tab__create_grid__error_label', '')
    display.set_visible('options_page__preseed_tab__create_grid', False)

    # Delete box
    stack = model.builder.get_object('options_page__preseed_tab__stack')
    scrolled_window = stack.get_visible_child()
    title = stack.child_get_property(scrolled_window, 'title')
    display.update_entry(
        'options_page__preseed_tab__delete_grid__entry',
        title)
    display.update_label(
        'options_page__preseed_tab__delete_grid__error_label',
        '')
    display.set_visible('options_page__preseed_tab__delete_grid', True)


def on_clicked__options_page__preseed_tab__delete_grid__button(widget):

    stack_name = 'options_page__preseed_tab__stack'
    stack = model.builder.get_object(stack_name)

    scrolled_window = stack.get_visible_child()
    title = stack.child_get_property(scrolled_window, 'title')
    filepath = stack.child_get_property(scrolled_window, 'name')

    timbrel_log.info(me,'Remove item from stack', stack_name)
    timbrel_log.info(me,'The title is', title)
    timbrel_log.info(me,'The name (filepath) is', filepath)

    # Only flag the file for deletion if it exits.
    if os.path.exists(filepath): model.delete_list.append(filepath)
    stack.remove(scrolled_window)

    # Show or hide widgets, as necessary.

    scrolled_window = stack.get_visible_child()
    ### scrolled_windows = stack.get_children()
    if scrolled_window:

        # Stack create button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__create_button',
            True)

        # Stack delete button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            True)

        # Stack
        display.set_visible('options_page__preseed_tab__stack', True)

        # Create box
        # display.update_entry('options_page__preseed_tab__create_grid__entry', '')
        # display.update_label('options_page__preseed_tab__create_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__create_grid', False)

        # Delete box
        # display.update_entry('options_page__preseed_tab__delete_grid__entry', '')
        # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__delete_grid', False)

    else:

        # Stack create button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__create_button',
            False)

        # Stack delete button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            False)

        # Stack
        display.set_visible('options_page__preseed_tab__stack', False)

        # Create box
        display.update_entry(
            'options_page__preseed_tab__create_grid__entry',
            '')
        display.update_label(
            'options_page__preseed_tab__create_grid__error_label',
            '')
        display.set_visible('options_page__preseed_tab__create_grid', True)

        # Delete box
        # display.update_entry('options_page__preseed_tab__delete_grid__entry', '')
        # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__delete_grid', False)


def on_event__options_page__preseed_tab__stack_sidebar(widget, event):

    stack = model.builder.get_object('options_page__preseed_tab__stack')

    # Show or hide widgets, as necessary.

    scrolled_window = stack.get_visible_child()
    ### scrolled_windows = stack.get_children()
    if scrolled_window:

        # Stack create button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__create_button',
            True)

        # Stack delete button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            True)

        # Stack
        display.set_visible('options_page__preseed_tab__stack', True)

        # Create box
        # display.update_entry('options_page__preseed_tab__create_grid__entry', '')
        # display.update_label('options_page__preseed_tab__create_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__create_grid', False)

        # Delete box
        # display.update_entry('options_page__preseed_tab__delete_grid__entry', '')
        # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__delete_grid', False)

    else:

        # Stack create button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__create_button',
            False)

        # Stack delete button
        display.set_sensitive(
            'options_page__preseed_tab__stack_sidebar__delete_button',
            False)

        # Stack
        display.set_visible('options_page__preseed_tab__stack', False)

        # Create box
        display.update_entry(
            'options_page__preseed_tab__create_grid__entry',
            '')
        display.update_label(
            'options_page__preseed_tab__create_grid__error_label',
            '')
        display.set_visible('options_page__preseed_tab__create_grid', True)

        # Delete box
        # display.update_entry('options_page__preseed_tab__delete_grid__entry', '')
        # display.update_label('options_page__preseed_tab__delete_grid__error_label', '')
        display.set_visible('options_page__preseed_tab__delete_grid', False)


####################################################################
# Options Page Handlers - Boot Configuration
####################################################################

# N/A

####################################################################
# Finish Page Handlers - Nautilus
####################################################################


def on_clicked__finish_page__custom_iso_image_directory_open_button(widget):

    # os.startfile(model.custom_iso_image_directory)
    # subprocess.Popen(['xdg-open', model.custom_iso_image_directory])
    # process = subprocess.Popen(['xdg-open', model.custom_iso_image_directory], preexec_fn=utilities.set_user_and_group(model.user_id, model.group_id))
    # subprocess.call(['xdg-open', model.custom_iso_image_directory])
    # timbrel_log.info(me,'The user, group for the current process is', 'User %s, Group %s' % (os.getuid(), os.getgid()))
    return
