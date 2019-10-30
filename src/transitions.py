#!/usr/bin/python3

########################################################################
#                                                                      #
# transitions.py                                                       #
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

import display
import handlers
import logger
import model
import utilities
import validators

import configparser
import glob
import os
import re
import time

MAXIMUM_ISO_SIZE_GIB = 8000.0
MAXIMUM_ISO_SIZE_BYTES = MAXIMUM_ISO_SIZE_GIB * 1073741824.0

# DEFAULT_BOOT_CONFIGURATIONS_STRING = 'boot/grub/grub.cfg,boot/grub/loopback.cfg,isolinux/isolinux.cfg,isolinux/txt.cfg'
DEFAULT_BOOT_CONFIGURATIONS_STRING = 'boot/grub/grub.cfg,boot/grub/loopback.cfg,isolinux/txt.cfg'

# General steps for each transiton.
#
# Note: Deactivating the current page is done by showing the spinner.
#       Activating a new page is done by hiding the spinner.
#
# [1] Perform functions on the current page, and deactivate the current page.
# [2] Prepare and display the new page.
# [3] Perform functions on the new page, and activate the new page.

########################################################################
# TransitionThread - Transition
########################################################################


# TODO: Update arguments to include button labels.
#       reset_buttons(is_quit_visible=False, is_back_visible=False,
#           is_next_visible=False, quit_button_label='Quit',
#           back_button_label='Back', next_button_label='Next')
def transition(
        old_page_name,
        new_page_name,
        quit_visible,
        back_visible,
        next_visible):
    logger.log_step('Performing requested transition action')
    logger.log_data('Transition from', old_page_name)
    logger.log_data('Transition to', new_page_name)

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # [2] Prepare and display the new page.

    display.show_page(old_page_name, new_page_name)
    display.reset_buttons(quit_visible, back_visible, next_visible)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


########################################################################
# TransitionThread - Transition "Next" Functions
########################################################################

# File Choosers
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

#
# Filechoosers
#


def transition__from__project_directory_page__project_directory_filechooser__to__project_directory_page(
        thread):

    dialog = model.builder.get_object(
        'project_directory_page__project_directory_filechooser')
    project_directory = dialog.get_filename()
    # project_directory = dialog.get_current_folder()
    display.update_entry(
        'project_directory_page__project_directory_entry',
        project_directory)

    display.set_sensitive('window', True)


def transition__from__original_iso_image_filepath_filechooser__to__new_project_page(
        thread):

    # Similar functions:
    # 1. transition__from__original_iso_image_filepath_filechooser__to__existing_project_page
    # 2. transition__from__original_iso_image_filepath_filechooser__to__new_project_page
    # 3. transition__from__existing_project_page__to__existing_project_page__radiobutton_3

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)

    dialog = model.builder.get_object(
        'new_project_page__original_iso_image_filepath_filechooser')

    # Original
    model.set_original_iso_image_filepath(dialog.get_filename())
    model.set_original_iso_image_filename(
        re.sub(r'.*/(.*$)',
               r'\1',
               model.original_iso_image_filepath))
    model.set_original_iso_image_directory(dialog.get_current_folder())

    # If the ISO image filepath is not mounted at the mount point, mount it. If
    # the ISO image filepath has changed, the previous image will be unmounted
    # before the new image is mounted at the mount point.
    if not utilities.is_mounted(model.original_iso_image_filepath,
                                model.original_iso_image_mount_point):
        # This function will unmount the existing image at the mount point.
        # This function will not mount the ISO image filepath if it is invalid.
        utilities.mount_iso_image(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point,
            thread)
    else:
        logger.log_data(
            'The original ISO image is already mounted at',
            model.original_iso_image_mount_point)

    if utilities.is_mounted(model.original_iso_image_filepath,
                            model.original_iso_image_mount_point):

        # Original
        model.set_original_iso_image_volume_id(
            utilities.get_iso_image_volume_id(
                model.original_iso_image_filepath,
                thread))
        model.set_original_iso_image_release_name(
            utilities.get_iso_image_release_name(
                model.original_iso_image_mount_point,
                thread))
        model.set_original_iso_image_disk_name(
            utilities.get_iso_image_disk_name(
                model.original_iso_image_mount_point,
                thread))
        model.set_casper_relative_directory(
            utilities.get_casper_relative_directory(
                model.original_iso_image_mount_point))

        # Custom
        model.set_custom_iso_image_version_number(
            utilities.create_custom_iso_image_version_number())
        model.set_custom_iso_image_filename(
            utilities.create_custom_iso_image_filename(
                model.original_iso_image_filename,
                model.custom_iso_image_version_number))
        model.set_custom_iso_image_directory(model.project_directory)
        model.set_custom_iso_image_filepath(
            os.path.join(
                model.custom_iso_image_directory,
                model.custom_iso_image_filename))
        model.set_custom_iso_image_volume_id(
            utilities.create_custom_iso_image_volume_id(
                model.original_iso_image_volume_id,
                model.custom_iso_image_version_number))
        model.set_custom_iso_image_release_name(
            utilities.create_custom_iso_image_release_name(
                model.original_iso_image_release_name))
        model.set_custom_iso_image_disk_name(
            utilities.create_custom_iso_image_disk_name(
                model.custom_iso_image_volume_id,
                model.custom_iso_image_release_name))
        model.set_custom_iso_image_md5_filename(
            utilities.create_custom_iso_image_md5_filename(
                model.custom_iso_image_filename))
        model.set_custom_iso_image_md5_filepath(
            os.path.join(
                model.custom_iso_image_directory,
                model.custom_iso_image_md5_filename))

        # Status
        model.set_is_success_copy_original_iso_files(False)
        model.set_is_success_extract_squashfs(False)

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'new_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'new_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'new_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'new_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'new_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'new_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'new_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'new_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'new_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'new_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'new_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_new_project_page()

    display.set_visible(
        'new_project_page__original_iso_image_filepath_filechooser',
        False)

    display.set_sensitive('window', True)

    model.set_propagate(True)


def transition__from__original_iso_image_filepath_filechooser__to__existing_project_page(
        thread):

    # Similar functions:
    # 1. transition__from__original_iso_image_filepath_filechooser__to__existing_project_page
    # 2. transition__from__original_iso_image_filepath_filechooser__to__new_project_page
    # 3. transition__from__existing_project_page__to__existing_project_page__radiobutton_3

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)

    dialog = model.builder.get_object(
        'existing_project_page__original_iso_image_filepath_filechooser')

    # Original
    model.set_original_iso_image_filepath(dialog.get_filename())
    model.set_original_iso_image_filename(
        re.sub(r'.*/(.*$)',
               r'\1',
               model.original_iso_image_filepath))
    model.set_original_iso_image_directory(dialog.get_current_folder())

    # If the ISO image filepath is not mounted at the mount point, mount it. If
    # the ISO image filepath has changed, the previous image will be unmounted
    # before the new image is mounted at the mount point.
    if not utilities.is_mounted(model.original_iso_image_filepath,
                                model.original_iso_image_mount_point):
        # This function will unmount the existing image at the mount point.
        # This function will not mount the ISO image filepath if it is invalid.
        utilities.mount_iso_image(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point,
            thread)
    else:
        logger.log_data(
            'The original ISO image is already mounted at',
            model.original_iso_image_mount_point)

    if utilities.is_mounted(model.original_iso_image_filepath,
                            model.original_iso_image_mount_point):

        # Original
        model.set_original_iso_image_volume_id(
            utilities.get_iso_image_volume_id(
                model.original_iso_image_filepath,
                thread))
        model.set_original_iso_image_release_name(
            utilities.get_iso_image_release_name(
                model.original_iso_image_mount_point,
                thread))
        model.set_original_iso_image_disk_name(
            utilities.get_iso_image_disk_name(
                model.original_iso_image_mount_point,
                thread))
        model.set_casper_relative_directory(
            utilities.get_casper_relative_directory(
                model.original_iso_image_mount_point))

        # Custom
        configuration = configparser.ConfigParser()
        configuration.optionxform = str
        configuration.read(model.configuration_filepath)

        model.set_custom_iso_image_version_number(
            configuration.get('Custom',
                              'custom_iso_image_version_number'))
        model.set_custom_iso_image_filename(
            configuration.get('Custom',
                              'custom_iso_image_filename'))
        model.set_custom_iso_image_directory(
            configuration.get('Custom',
                              'custom_iso_image_directory'))
        model.set_custom_iso_image_filepath(
            os.path.join(
                model.custom_iso_image_directory,
                model.custom_iso_image_filename))
        model.set_custom_iso_image_volume_id(
            configuration.get('Custom',
                              'custom_iso_image_volume_id'))
        model.set_custom_iso_image_release_name(
            configuration.get('Custom',
                              'custom_iso_image_release_name'))
        model.set_custom_iso_image_disk_name(
            configuration.get('Custom',
                              'custom_iso_image_disk_name'))
        model.set_custom_iso_image_md5_filename(
            configuration.get('Custom',
                              'custom_iso_image_md5_filename'))
        model.set_custom_iso_image_md5_filepath(
            os.path.join(
                model.custom_iso_image_directory,
                model.custom_iso_image_md5_filename))

        # Status
        stored_original_iso_image_filepath = os.path.join(
            configuration.get('Original',
                              'original_iso_image_directory'),
            configuration.get('Original',
                              'original_iso_image_filename'))
        if stored_original_iso_image_filepath != model.original_iso_image_filepath:
            # If the stored original iso image filepath is not the same as the
            # new original iso image filepath, then then the original iso files
            # were not successfully coppied.
            model.set_is_success_copy_original_iso_files(False)
        else:
            # If the stored original iso image filepath is the same as the new
            # original iso image filepath, then use the prevously stored status
            # if the original iso files were or were not successfully coppied.
            model.set_is_success_copy_original_iso_files(
                configuration.getboolean(
                    'Status',
                    'is_success_copy_original_iso_files',
                    fallback=True))

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'existing_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'existing_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'existing_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'existing_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'existing_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'existing_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'existing_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'existing_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page()

    display.set_visible(
        'existing_project_page__original_iso_image_filepath_filechooser',
        False)

    display.set_sensitive('window', True)

    model.set_propagate(True)


def transition__from__custom_iso_image_directory_filechooser__to__new_project_page(
        thread):

    dialog = model.builder.get_object(
        'new_project_page__custom_iso_image_directory_filechooser')
    custom_iso_image_directory = dialog.get_filename()
    # custom_iso_image_directory = dialog.get_current_folder()
    display.update_entry(
        'new_project_page__custom_iso_image_directory_entry',
        custom_iso_image_directory)

    display.set_visible(
        'new_project_page__custom_iso_image_directory_filechooser',
        False)

    display.set_sensitive('window', True)


def transition__from__custom_iso_image_directory_filechooser__to__existing_project_page(
        thread):

    dialog = model.builder.get_object(
        'existing_project_page__custom_iso_image_directory_filechooser')
    custom_iso_image_directory = dialog.get_filename()
    # custom_iso_image_directory = dialog.get_current_folder()
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        custom_iso_image_directory)

    display.set_visible(
        'existing_project_page__custom_iso_image_directory_filechooser',
        False)

    display.set_sensitive('window', True)


#
# Project Directory Page
#


def transition__from__project_directory_page__to__new_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)
    display.show_spinner()
    display.reset_buttons()

    # Original
    model.set_original_iso_image_filepath(
        '')  # Aggregated value; not displayed.
    model.set_original_iso_image_filename('')
    model.set_original_iso_image_directory('')
    model.set_original_iso_image_volume_id('')
    model.set_original_iso_image_release_name('')
    model.set_original_iso_image_disk_name('')

    # Custom
    model.set_custom_iso_image_version_number('')
    model.set_custom_iso_image_filename('')
    model.set_custom_iso_image_directory('')
    model.set_custom_iso_image_filepath('')  # Aggregated value; not displayed.
    model.set_custom_iso_image_volume_id('')
    model.set_custom_iso_image_release_name('')
    model.set_custom_iso_image_disk_name('')
    model.set_custom_iso_image_md5_filename(
        '')  # Aggregated value; not displayed.
    model.set_custom_iso_image_md5_filepath(
        '')  # Aggregated value; not displayed.

    # Status
    model.set_is_success_copy_original_iso_files(False)
    model.set_is_success_extract_squashfs(False)

    # Options
    boot_configurations_string = DEFAULT_BOOT_CONFIGURATIONS_STRING
    boot_configurations = []
    for boot_configuration in boot_configurations_string.split(','):
        boot_configuration = boot_configuration.strip(' ' + os.sep)
        filepath = os.path.join(
            model.custom_live_iso_directory,
            boot_configuration)
        if os.path.exists(filepath):
            boot_configurations.append(boot_configuration)
    model.set_boot_configurations(boot_configurations)

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'new_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'new_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'new_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'new_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'new_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'new_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'new_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'new_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'new_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'new_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'new_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # Activate radio button 2 as the default option (continue customizing the
    # existing project) when the existing project page is displyed.
    # The handler on_toggled__existing_project_page__radiobutton() is called
    # whenever the radiobutton is toggled; however the function will not
    # execute, because model.propagate is False.
    display.activate_radiobutton('existing_project_page__radiobutton_2', True)

    # Transition to the New Project page.
    display.show_page('project_directory_page', 'new_project_page')
    display.reset_buttons(True, True, False)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_new_project_page()

    display.hide_spinner()

    model.set_propagate(True)


def transition__from__project_directory_page__to__existing_project_page(
        thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)
    display.show_spinner()
    display.reset_buttons()

    # Create the configuration.
    configuration = configparser.ConfigParser()
    configuration.optionxform = str
    configuration.read(model.configuration_filepath)

    # Original
    model.set_original_iso_image_filename(
        configuration.get('Original',
                          'original_iso_image_filename'))
    model.set_original_iso_image_directory(
        configuration.get('Original',
                          'original_iso_image_directory'))
    model.set_original_iso_image_filepath(
        os.path.join(
            model.original_iso_image_directory,
            model.original_iso_image_filename))

    # If the ISO image filepath is not mounted at the mount point, mount it. If
    # the ISO image filepath has changed, the previous image will be unmounted
    # before the new image is mounted at the mount point.
    is_mounted = utilities.is_mounted(
        model.original_iso_image_filepath,
        model.original_iso_image_mount_point)
    if not is_mounted:
        # This function will unmount the existing image at the mount point.
        # This function will not mount the ISO image filepath if it is invalid.
        utilities.mount_iso_image(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point,
            thread)

    # if utilities.is_mounted(model.original_iso_image_filepath, model.original_iso_image_mount_point):
    # model.set_original_iso_image_volume_id(utilities.get_iso_image_volume_id(model.original_iso_image_filepath, thread))
    model.set_original_iso_image_volume_id(
        configuration.get('Original',
                          'original_iso_image_volume_id'))
    # model.set_original_iso_image_release_name(utilities.get_iso_image_release_name(model.original_iso_image_mount_point, thread))
    model.set_original_iso_image_release_name(
        configuration.get('Original',
                          'original_iso_image_release_name'))
    # model.set_original_iso_image_disk_name(utilities.get_iso_image_disk_name(model.original_iso_image_mount_point, thread))
    model.set_original_iso_image_disk_name(
        configuration.get('Original',
                          'original_iso_image_disk_name'))
    ### TODO: This crashes if the original ISO does not exist.
    ###       Solution is to check if ISO exists before enabling Next button, when project directory is selected.
    ###       Another option might be to go to the existing project page, but force the user to select a new ISO.
    ###       This would mean setting the relative casper directory later on.
    model.set_casper_relative_directory(
        utilities.get_casper_relative_directory(
            model.original_iso_image_mount_point))

    # Custom
    model.set_custom_iso_image_version_number(
        configuration.get('Custom',
                          'custom_iso_image_version_number'))
    model.set_custom_iso_image_filename(
        configuration.get('Custom',
                          'custom_iso_image_filename'))
    model.set_custom_iso_image_directory(
        configuration.get('Custom',
                          'custom_iso_image_directory'))
    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))
    model.set_custom_iso_image_volume_id(
        configuration.get('Custom',
                          'custom_iso_image_volume_id'))
    model.set_custom_iso_image_release_name(
        configuration.get('Custom',
                          'custom_iso_image_release_name'))
    model.set_custom_iso_image_disk_name(
        configuration.get('Custom',
                          'custom_iso_image_disk_name'))
    model.set_custom_iso_image_md5_filename(
        configuration.get('Custom',
                          'custom_iso_image_md5_filename'))
    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    # Status
    model.set_is_success_copy_original_iso_files(
        configuration.getboolean(
            'Status',
            'is_success_copy_original_iso_files',
            fallback=True))
    model.set_is_success_extract_squashfs(
        configuration.getboolean(
            'Status',
            'is_success_extract_squashfs',
            fallback=True))

    # Options
    boot_configurations_string = configuration.get(
        'Options',
        'boot_configurations',
        fallback=DEFAULT_BOOT_CONFIGURATIONS_STRING)
    boot_configurations = []
    for boot_configuration in boot_configurations_string.split(','):
        boot_configuration = boot_configuration.strip(' ' + os.sep)
        filepath = os.path.join(
            model.custom_live_iso_directory,
            boot_configuration)
        if os.path.exists(filepath):
            boot_configurations.append(boot_configuration)
    model.set_boot_configurations(boot_configurations)

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'existing_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'existing_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'existing_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'existing_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'existing_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'existing_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'existing_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'existing_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # Activate radio button 1 as the default option (create a disk image from
    # the existing project) when the existing project page is displayed.
    # The handler on_toggled__existing_project_page__radiobutton() is called
    # whenever the radiobutton is toggled; however the function will not
    # execute, because model.propagate is False.
    display.activate_radiobutton('existing_project_page__radiobutton_1', True)

    # Transition to the Existing Project page.
    display.show_page('project_directory_page', 'existing_project_page')
    display.reset_buttons(True, True, False)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page()

    display.hide_spinner()

    model.set_propagate(True)


#
# Shared Functions:
# - New Project Page
# - Existing Project Page
# - Unsquashfs Page
# - Terminal Page
#


def _transition__from__project_page__to__unsquashfs_page(
        old_page_name,
        thread):

    # TODO: These functions do not exist. Revise comment.
    # This is the same as transition__from__new_project_page__to__unsquashfs_page(thread)
    # This is the same as transition__from__existing_project_page__to__unsquashfs_page(thread)

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Save the configuration (since it may have changed).
    # Changes are are not persisted on the previous page, so the configuration
    # may be saved after the user clicks Next on the previous page.
    utilities.save_configuration()

    # [2] Prepare and display the new page.

    # display.hide_spinner()

    # Setup the Copy Original ISO Files section.
    display.update_label(
        'unsquashfs_page__copy_original_iso_files_label',
        'Copy ISO files from the original disk image:')
    display.update_label(
        'unsquashfs_page__copy_original_iso_files_original_disk_image_label',
        '%s' % model.original_iso_image_filepath)
    display.update_progressbar_percent(
        'unsquashfs_page__copy_original_iso_files_progressbar',
        0)
    display.update_progressbar_text(
        'unsquashfs_page__copy_original_iso_files_progressbar',
        '')
    display.set_label_error(
        'unsquashfs_page__copy_original_iso_files_result_label',
        False)
    display.update_label(
        'unsquashfs_page__copy_original_iso_files_result_label',
        '...')
    display.update_status(
        'unsquashfs_page__copy_original_iso_files',
        display.BULLET)
    display.set_visible(
        'unsquashfs_page__copy_original_iso_files_section',
        True)

    # Setup the Unsquashfs section.
    display.update_label(
        'unsquashfs_page__unsquashfs_original_disk_image_label',
        '%s' % model.original_iso_image_filepath)
    display.update_progressbar_percent(
        'unsquashfs_page__unsquashfs_progressbar',
        0)
    display.update_progressbar_text(
        'unsquashfs_page__unsquashfs_progressbar',
        '')
    display.set_label_error('unsquashfs_page__unsquashfs_result_label', False)
    display.update_label('unsquashfs_page__unsquashfs_result_label', '...')
    display.update_status('unsquashfs_page__unsquashfs', display.BULLET)
    display.set_visible('unsquashfs_page__unsquashfs_section', True)

    # Transition to the Unsquashfs page.
    display.show_page(old_page_name, 'unsquashfs_page')
    display.reset_buttons(True, True, False)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()

    # Perform actions in the Copy Original ISO Files section.

    display.update_status(
        'unsquashfs_page__copy_original_iso_files',
        display.PROCESSING)
    time.sleep(0.25)

    if model.is_success_copy_original_iso_files:
        display.update_progressbar_percent(
            'unsquashfs_page__copy_original_iso_files_progressbar',
            100)
        display.set_label_error(
            'unsquashfs_page__copy_original_iso_files_result_label',
            False)
        display.update_label(
            'unsquashfs_page__copy_original_iso_files_result_label',
            'Using previously copied original ISO files.')
        display.update_status(
            'unsquashfs_page__copy_original_iso_files',
            display.OK)
    else:
        # Copy original ISO files.
        is_success = utilities.copy_original_iso_files(thread)
        model.set_is_success_copy_original_iso_files(is_success)

        if model.is_success_copy_original_iso_files:
            # Options (configurations)
            boot_configurations_string = DEFAULT_BOOT_CONFIGURATIONS_STRING
            boot_configurations = []
            for boot_configuration in boot_configurations_string.split(','):
                boot_configuration = boot_configuration.strip(' ' + os.sep)
                filepath = os.path.join(
                    model.custom_live_iso_directory,
                    boot_configuration)
                if os.path.exists(filepath):
                    boot_configurations.append(boot_configuration)
            model.set_boot_configurations(boot_configurations)

            # Display the Copy Original ISO Files section.
            display.set_label_error(
                'unsquashfs_page__copy_original_iso_files_result_label',
                False)
            display.update_label(
                'unsquashfs_page__copy_original_iso_files_result_label',
                'All original ISO files have been copied.')
            display.update_status(
                'unsquashfs_page__copy_original_iso_files',
                display.OK)
        else:
            display.set_label_error(
                'unsquashfs_page__copy_original_iso_files_result_label',
                True)
            display.update_label(
                'unsquashfs_page__copy_original_iso_files_result_label',
                'Unable to copy original ISO files.')
            display.update_status(
                'unsquashfs_page__copy_original_iso_files',
                display.ERROR)

    time.sleep(0.50)

    # Perform actions in the Unsquashfs section.

    display.update_status('unsquashfs_page__unsquashfs', display.PROCESSING)
    time.sleep(0.25)

    if model.is_success_extract_squashfs:
        display.update_progressbar_percent(
            'unsquashfs_page__unsquashfs_progressbar',
            100)
        display.set_label_error(
            'unsquashfs_page__unsquashfs_result_label',
            False)
        display.update_label(
            'unsquashfs_page__unsquashfs_result_label',
            'Using previously extracted compressed Linux file system.')
        display.update_status('unsquashfs_page__unsquashfs', display.OK)
    else:
        # Clear the terminal because the history will no longer be valid.
        terminal = model.builder.get_object('terminal_page__terminal')
        terminal.reset(True, True)

        # Extract filesystem.squashfs.
        is_success = utilities.extract_squashfs(thread)
        model.set_is_success_extract_squashfs(is_success)

        if model.is_success_extract_squashfs:
            # Display the Unsquashfs section.
            display.set_label_error(
                'unsquashfs_page__unsquashfs_result_label',
                False)
            display.update_label(
                'unsquashfs_page__unsquashfs_result_label',
                'The compressed Linux file system has been extracted.')
            display.update_status('unsquashfs_page__unsquashfs', display.OK)
        else:
            display.set_label_error(
                'unsquashfs_page__unsquashfs_result_label',
                True)
            display.update_label(
                'unsquashfs_page__unsquashfs_result_label',
                'Unable to extract the compressed Linux file system.')
            display.update_status('unsquashfs_page__unsquashfs', display.ERROR)

    time.sleep(1.00)

    # Save the configuration (since it may have changed).
    # Since this page persists changes (such as copying original iso files or
    # extracting squashfs) the configuration must be persisted on this page as
    # well.
    utilities.save_configuration()

    is_page_complete = (
        model.is_success_copy_original_iso_files
        and model.is_success_extract_squashfs)

    # display.reset_buttons(True, True, is_page_complete)

    return is_page_complete


def _transition__from__unknown_page__to__options_page(old_page_name, thread):

    # Similar functions:
    # 1. _transition__from__unsquashfs_page__to__options_page
    # 2. transition__from__terminal_page__to__options_page

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Not necessary: Save the configuration (since it may have changed).
    # The configuration is already saved on the previous page, since changes are
    # persisted on the previous page (such as copying original iso files or
    # extracting squashfs).
    # utilities.save_configuration()

    # Get a list of installed packages.
    # This function must be invoked before exit_chroot_environment() because
    # exiting the chroot environment kills all processes using the custom
    # squashfs directory. In some cases, create_installed_packages_list() gets
    # killed when it is invoked immediately after exit_chroot_environment().
    installed_packages_list = utilities.create_installed_packages_list(thread)

    if old_page_name == 'terminal_page':

        # Exit the chroot environment.

        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Exiting from the chroot environment...')
        display.set_visible('terminal_page__exit_terminal_label', True)

        # Disconnect terminal exit handler.
        if model.handler_id:
            terminal = model.builder.get_object('terminal_page__terminal')
            terminal.disconnect(model.handler_id)
            model.set_handler_id(None)

        utilities.exit_chroot_environment(thread)

        is_chroot = utilities.check_chroot(thread)

        if not is_chroot:
            # Disable input to the terminal.
            display.set_sensitive('terminal_page__terminal', False)
            display.set_label_error(
                'terminal_page__exit_terminal_label',
                False)
            display.update_label(
                'terminal_page__exit_terminal_label',
                'Successfully exited from the chroot environment.')
            display.set_visible('terminal_page__exit_terminal_label', True)
        else:
            # Enable input to the terminal.
            display.set_sensitive('terminal_page__terminal', True)
            display.set_label_error('terminal_page__exit_terminal_label', True)
            display.update_label(
                'terminal_page__exit_terminal_label',
                'Unable to exit from the chroot environment.')
            display.set_visible('terminal_page__exit_terminal_label', True)

        time.sleep(1.00)

    # [2] Prepare and display the new page.

    # Transition to the Manage Options page.

    #
    # Manifest tab
    #

    # Create filesystem manifest file.
    utilities.create_filesystem_manifest_file(installed_packages_list)

    package_count = len(installed_packages_list)
    # TODO: Show number of packages installed.
    # display.update_label(
    #     'create_manifest_page__create_filesystem_manifest_result_label',
    #     'There are %s packages installed.' % package_count)

    # Create list of removable packages for a typical install.
    filename = 'filesystem.manifest-remove'
    is_exists = utilities.is_exists_filesystem_manifest_remove(filename)
    removable_packages_list_1 = utilities.get_removable_packages_list(
        filename) if is_exists else []

    # Create list of removable packages for a minimal install.
    filename = 'filesystem.manifest-minimal-remove'
    is_exists = utilities.is_exists_filesystem_manifest_remove(filename)
    removable_packages_list_2 = utilities.get_removable_packages_list(
        filename) if is_exists else []

    package_details_list = utilities.create_package_details_list(
        installed_packages_list,
        removable_packages_list_1,
        removable_packages_list_2)

    if removable_packages_list_2:
        display.set_column_visible(
            'options_page__package_manifest_tab__remove_2_treeviewcolumn',
            True)
    else:
        display.set_column_visible(
            'options_page__package_manifest_tab__remove_2_treeviewcolumn',
            False)

    display.update_liststore(
        'options_page__package_manifest_tab__liststore',
        package_details_list)

    model.undo_index = 0
    model.undo_list = []
    display.set_sensitive(
        'options_page__package_manifest_tab__revert_button',
        False)
    display.set_sensitive(
        'options_page__package_manifest_tab__undo_button',
        False)
    display.set_sensitive(
        'options_page__package_manifest_tab__redo_button',
        False)

    #
    # Linux kernels tab
    #

    # Get the list of linux kernels.
    # .../squashfs-root/boot/vmlinuz-*; initrd.img-*
    directory_1 = os.path.join(model.custom_squashfs_directory, 'boot')
    # .../original-iso-mount/casper/vmlinuz.efi; initrd.lz
    directory_2 = os.path.join(
        model.original_iso_image_mount_point,
        model.casper_relative_directory)
    kernel_details_list = utilities.create_kernel_details_list(
        directory_1,
        directory_2)

    # TODO: See if this code can be replaced with elements in cubic.ui
    # REFERENCE: https://whyareyoureadingthisurl.wordpress.com/2012/01/21/howto-pack-gtk-cellrenderers-vertically-in-a-gtk-treeview/
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    column = model.builder.get_object(
        'options_page__linux_kernels_tab__treeviewcolumn_2')
    area = column.get_area()
    area.set_orientation(Gtk.Orientation.VERTICAL)
    display.update_liststore(
        'options_page__linux_kernels_tab__liststore',
        kernel_details_list)

    #
    # Preseed tab
    #

    stack_name = 'options_page__preseed_tab__stack'

    model.delete_list = []
    ### TODO: Only read text files.
    search_filepath = os.path.join(
        model.custom_live_iso_directory,
        'preseed',
        '*')
    filepaths = glob.glob(search_filepath)
    filepaths.sort()

    display.add_to_stack(stack_name, filepaths)

    if filepaths:

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

    #
    # Boot configuration tab
    #

    filepaths = []
    for boot_configuration in model.boot_configurations:
        filepath = os.path.join(
            model.custom_live_iso_directory,
            boot_configuration)
        filepaths.append(filepath)

    # Get the selected kernel.
    for selected_index, kernel_details in enumerate(kernel_details_list):
        if kernel_details[7]: break
    else: selected_index = 0
    logger.log_data('The selected kernel is index number', selected_index)

    # Add files to the stack, and search and replace text.
    stack_name = 'options_page__boot_configuration_tab__stack'
    search_text_1 = r'/vmlinuz\S*'
    replacement_text_1 = '/%s' % kernel_details_list[selected_index][2]
    search_text_2 = r'/initrd\S*'
    replacement_text_2 = '/%s' % kernel_details_list[selected_index][4]
    display.add_to_stack(
        stack_name,
        filepaths,
        (search_text_1,
         replacement_text_1),
        (search_text_2,
         replacement_text_2))

    # Transition to the Manage Options page.
    display.show_page(old_page_name, 'options_page')
    display.reset_buttons(True, True, True, next_button_label='Generate')

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


#
# New Project Page
#


def transition__from__new_project_page__to__terminal_page(thread):

    if _transition__from__project_page__to__unsquashfs_page('new_project_page',
                                                            thread):
        _transition__from__unsquashfs_page__to__terminal_page(thread)


#
# Existing Project Page
#


def transition__from__existing_project_page__to__existing_project_page(thread):

    if model.builder.get_object(
            'existing_project_page__radiobutton_1').get_active():
        _transition__from__existing_project_page__to__existing_project_page__radiobutton_1(
            thread)
    elif model.builder.get_object(
            'existing_project_page__radiobutton_2').get_active():
        _transition__from__existing_project_page__to__existing_project_page__radiobutton_2(
            thread)
    elif model.builder.get_object(
            'existing_project_page__radiobutton_3').get_active():
        _transition__from__existing_project_page__to__existing_project_page__radiobutton_3(
            thread)


def _transition__from__existing_project_page__to__existing_project_page__radiobutton_1(
        thread):

    display.set_sensitive(
        'existing_project_page__original_iso_image_filepath_filechooser__open_button',
        True)
    display.reset_buttons(True, True, False)
    validators.validate_existing_project_page()


def _transition__from__existing_project_page__to__existing_project_page__radiobutton_2(
        thread):

    display.set_sensitive(
        'existing_project_page__original_iso_image_filepath_filechooser__open_button',
        True)
    display.reset_buttons(True, True, False)
    validators.validate_existing_project_page()


def _transition__from__existing_project_page__to__existing_project_page__radiobutton_3(
        thread):

    # Similar functions:
    # 1. transition__from__original_iso_image_filepath_filechooser__to__existing_project_page
    # 2. transition__from__original_iso_image_filepath_filechooser__to__new_project_page
    # 3. transition__from__existing_project_page__to__existing_project_page__radiobutton_3

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)
    display.show_spinner()
    display.reset_buttons()

    configuration = configparser.ConfigParser()
    configuration.optionxform = str
    configuration.read(model.configuration_filepath)

    # Original
    model.set_original_iso_image_filename(
        configuration.get('Original',
                          'original_iso_image_filename'))
    model.set_original_iso_image_directory(
        configuration.get('Original',
                          'original_iso_image_directory'))
    model.set_original_iso_image_filepath(
        os.path.join(
            model.original_iso_image_directory,
            model.original_iso_image_filename))

    # If the ISO image filepath is not mounted at the mount point, mount it. If
    # the ISO image filepath has changed, the previous image will be unmounted
    # before the new image is mounted at the mount point.
    if not utilities.is_mounted(model.original_iso_image_filepath,
                                model.original_iso_image_mount_point):
        # This function will unmount the existing image at the mount point.
        # This function will not mount the ISO image filepath if it is invalid.
        utilities.mount_iso_image(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point,
            thread)
    else:
        logger.log_data(
            'The original ISO image is already mounted at',
            model.original_iso_image_mount_point)

    if utilities.is_mounted(model.original_iso_image_filepath,
                            model.original_iso_image_mount_point):

        # Original
        model.set_original_iso_image_volume_id(
            configuration.get('Original',
                              'original_iso_image_volume_id'))
        model.set_original_iso_image_release_name(
            configuration.get('Original',
                              'original_iso_image_release_name'))
        model.set_original_iso_image_disk_name(
            configuration.get('Original',
                              'original_iso_image_disk_name'))
        model.set_casper_relative_directory(
            utilities.get_casper_relative_directory(
                model.original_iso_image_mount_point))

    # Custom
    model.set_custom_iso_image_version_number(
        configuration.get('Custom',
                          'custom_iso_image_version_number'))
    model.set_custom_iso_image_filename(
        configuration.get('Custom',
                          'custom_iso_image_filename'))
    model.set_custom_iso_image_directory(
        configuration.get('Custom',
                          'custom_iso_image_directory'))
    model.set_custom_iso_image_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_filename))
    model.set_custom_iso_image_volume_id(
        configuration.get('Custom',
                          'custom_iso_image_volume_id'))
    model.set_custom_iso_image_release_name(
        configuration.get('Custom',
                          'custom_iso_image_release_name'))
    model.set_custom_iso_image_disk_name(
        configuration.get('Custom',
                          'custom_iso_image_disk_name'))
    model.set_custom_iso_image_md5_filename(
        configuration.get('Custom',
                          'custom_iso_image_md5_filename'))
    model.set_custom_iso_image_md5_filepath(
        os.path.join(
            model.custom_iso_image_directory,
            model.custom_iso_image_md5_filename))

    # Status
    model.set_is_success_copy_original_iso_files(
        configuration.getboolean(
            'Status',
            'is_success_copy_original_iso_files',
            fallback=True))

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'existing_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'existing_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'existing_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'existing_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    display.set_sensitive(
        'existing_project_page__original_iso_image_filepath_filechooser__open_button',
        False)

    # Display custom values.
    display.update_entry(
        'existing_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'existing_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'existing_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'existing_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # display.set_sensitive('existing_project_page__custom_iso_image_directory_filechooser__open_button', False)

    # Transition to the Existing Project page.
    # display.show_page('project_directory_page', 'existing_project_page')
    display.reset_buttons(True, True, False)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page_for_delete()

    display.hide_spinner()

    model.set_propagate(True)


def transition__from__existing_project_page__to__options_page(thread):

    if _transition__from__project_page__to__unsquashfs_page(
            'existing_project_page',
            thread):
        _transition__from__unsquashfs_page__to__options_page(thread)


def transition__from__existing_project_page__to__terminal_page(thread):

    if _transition__from__project_page__to__unsquashfs_page(
            'existing_project_page',
            thread):
        _transition__from__unsquashfs_page__to__terminal_page(thread)


def transition__from__existing_project_page__to__delete_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # [2] Prepare and display the new page.

    if os.path.exists(model.configuration_filepath):
        display.update_status(
            'delete_project_page__configuration_file',
            display.BULLET)
        display.set_visible(
            'delete_project_page__configuration_file_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__configuration_file_section',
            False)

    if os.path.exists(model.original_iso_image_mount_point):
        display.update_status(
            'delete_project_page__original_iso_image_mount_point',
            display.BULLET)
        display.set_visible(
            'delete_project_page__original_iso_image_mount_point_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__custom_squashfs_directory_section',
            False)

    if os.path.exists(model.custom_squashfs_directory):
        display.update_status(
            'delete_project_page__custom_squashfs_directory',
            display.BULLET)
        display.set_visible(
            'delete_project_page__custom_squashfs_directory_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__custom_squashfs_directory_section',
            False)

    if os.path.exists(model.custom_live_iso_directory):
        display.update_status(
            'delete_project_page__custom_live_iso_directory',
            display.BULLET)
        display.set_visible(
            'delete_project_page__custom_live_iso_directory_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__custom_live_iso_directory_section',
            False)

    # Only delete the custom ISO image if it is directly under the project directory.
    filepath = os.path.join(
        model.project_directory,
        model.custom_iso_image_filename)
    if os.path.exists(filepath):
        display.update_status(
            'delete_project_page__custom_iso_image_filename',
            display.BULLET)
        display.update_label(
            'delete_project_page__custom_iso_image_filename_filepath',
            filepath)
        display.set_visible(
            'delete_project_page__custom_iso_image_filename_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__custom_iso_image_filename_section',
            False)

    # Only delete the custom ISO image MD5 file if it is directly under the project directory.
    filepath = os.path.join(
        model.project_directory,
        model.custom_iso_image_md5_filename)
    if os.path.exists(filepath):
        display.update_status(
            'delete_project_page__custom_iso_image_md5_filename',
            display.BULLET)
        display.update_label(
            'delete_project_page__custom_iso_image_md5_filename_filepath',
            filepath)
        display.set_visible(
            'delete_project_page__custom_iso_image_md5_filename_section',
            True)
    else:
        display.set_visible(
            'delete_project_page__custom_iso_image_md5_filename_section',
            False)

    # Transition to the Delete Project page.
    display.show_page('existing_project_page', 'delete_project_page')
    display.reset_buttons(
        True,
        True,
        True,
        back_button_label='Cancel',
        next_button_label='Delete')

    # [3] Perform functions on the new page, and activate the new page.
    display.hide_spinner()


#
# Delete Project Page
#


def transition__from__delete_project_page__to__new_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)
    display.reset_buttons(True, False, False)

    # TODO: Add checks if delete actions were successful.
    if os.path.exists(model.configuration_filepath):

        display.update_status(
            'delete_project_page__configuration_file',
            display.PROCESSING)
        time.sleep(0.25)

        # Delete file, cubic.conf.
        logger.log_data(
            'About to delete configuration file',
            model.configuration_filepath)
        utilities.delete_file(model.configuration_filepath, thread)
        display.update_status(
            'delete_project_page__configuration_file',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__configuration_file',
            display.BULLET)
        display.set_visible(
            'delete_project_page__configuration_file_section',
            False)

    if os.path.exists(model.original_iso_image_mount_point):

        display.update_status(
            'delete_project_page__original_iso_image_mount_point',
            display.PROCESSING)
        time.sleep(0.25)

        # Unmount the original ISO image and delete the mount point.
        logger.log_data(
            'About to delete original ISO image mount point',
            model.original_iso_image_mount_point)
        utilities.delete_iso_mount(
            model.original_iso_image_mount_point,
            thread)
        display.update_status(
            'delete_project_page__original_iso_image_mount_point',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__original_iso_image_mount_point',
            display.BULLET)
        display.set_visible(
            'delete_project_page__original_iso_image_mount_point_section',
            False)

    if os.path.exists(model.custom_squashfs_directory):

        display.update_status(
            'delete_project_page__custom_squashfs_directory',
            display.PROCESSING)
        time.sleep(0.25)

        # Delete directory, squashfs-root.
        logger.log_data(
            'About to delete custom squashfs directory',
            model.custom_squashfs_directory)
        utilities.delete_file(model.custom_squashfs_directory, thread)
        display.update_status(
            'delete_project_page__custom_squashfs_directory',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__custom_squashfs_directory',
            display.BULLET)
        display.set_visible(
            'delete_project_page__original_iso_image_mount_point_section',
            False)

    if os.path.exists(model.custom_live_iso_directory):
        display.update_status(
            'delete_project_page__custom_live_iso_directory',
            display.PROCESSING)
        time.sleep(0.25)

        # Delete directory, custom-live-iso.
        logger.log_data(
            'About to delete custom live ISO directory',
            model.custom_live_iso_directory)
        utilities.delete_file(model.custom_live_iso_directory, thread)
        display.update_status(
            'delete_project_page__custom_live_iso_directory',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__custom_live_iso_directory',
            display.BULLET)
        display.set_visible(
            'delete_project_page__custom_live_iso_directory_section',
            False)

    # Only delete the custom ISO image if it is directly under the project directory.
    filepath = os.path.join(
        model.project_directory,
        model.custom_iso_image_filename)
    if os.path.exists(filepath):

        display.update_status(
            'delete_project_page__custom_iso_image_filename',
            display.PROCESSING)
        time.sleep(0.25)

        # Delete file, *.iso.
        logger.log_data('About to delete custom ISO image file', filepath)
        utilities.delete_file(filepath, thread)
        display.update_status(
            'delete_project_page__custom_iso_image_filename',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__custom_iso_image_filename',
            display.BULLET)
        display.set_visible(
            'delete_project_page__custom_iso_image_filename_section',
            False)

    # Only delete the MD5 file if it is directly under the project directory.
    filepath = os.path.join(
        model.project_directory,
        model.custom_iso_image_md5_filename)
    if os.path.exists(filepath):

        display.update_status(
            'delete_project_page__custom_iso_image_md5_filename',
            display.PROCESSING)
        time.sleep(0.25)

        # Delete file, *.md5.
        logger.log_data('About to delete custom ISO image MD5 file', filepath)
        utilities.delete_file(filepath, thread)
        display.update_status(
            'delete_project_page__custom_iso_image_md5_filename',
            display.OK)
        time.sleep(0.25)

    else:

        display.update_status(
            'delete_project_page__custom_iso_image_md5_filename',
            display.BULLET)
        display.set_visible(
            'delete_project_page__custom_iso_image_md5_filename_section',
            False)

    # Reset all global variables before transitioning to new project page.
    display.show_spinner()
    display.reset_buttons()

    # Original
    model.set_original_iso_image_filepath(
        '')  # Aggregated value; not displayed.
    model.set_original_iso_image_filename('')
    model.set_original_iso_image_directory('')
    model.set_original_iso_image_volume_id('')
    model.set_original_iso_image_release_name('')
    model.set_original_iso_image_disk_name('')

    # Custom
    model.set_custom_iso_image_version_number('')
    model.set_custom_iso_image_filename('')
    model.set_custom_iso_image_directory('')
    model.set_custom_iso_image_filepath('')  # Aggregated value; not displayed.
    model.set_custom_iso_image_volume_id('')
    model.set_custom_iso_image_release_name('')
    model.set_custom_iso_image_disk_name('')
    model.set_custom_iso_image_md5_filename(
        '')  # Aggregated value; not displayed.
    model.set_custom_iso_image_md5_filepath(
        '')  # Aggregated value; not displayed.

    # Status
    model.set_is_success_copy_original_iso_files(False)
    model.set_is_success_extract_squashfs(False)

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'new_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'new_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'new_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'new_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'new_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'new_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'new_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'new_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'new_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'new_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'new_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # Activate radio button 2 as the default option (continue customizing the
    # existing project) when the existing project page is displayed.
    # The handler on_toggled__existing_project_page__radiobutton() is called
    # whenever the radiobutton is toggled; however the function will not
    # execute, because model.propagate is False.
    display.activate_radiobutton('existing_project_page__radiobutton_2', True)

    # Transition to the New Project page.
    display.show_page('delete_project_page', 'new_project_page')
    display.reset_buttons(True, True, False)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_new_project_page()

    display.hide_spinner()

    model.set_propagate(True)


#
# Unsquashfs Page
#


def _transition__from__unsquashfs_page__to__terminal_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Save the configuration (since it may have changed).
    utilities.save_configuration()

    # [2] Prepare and display the new page.

    # display.set_label_error('terminal_page__exit_terminal_label', False)
    # display.update_label(
    #     'terminal_page__exit_terminal_label',
    #     '...')
    # display.set_visible('terminal_page__exit_terminal_label', True)

    # Transition to the Terminal page.
    display.show_page('unsquashfs_page', 'terminal_page')

    # [3] Perform functions on the new page, and activate the new page.

    # Enter the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Entering the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    utilities.prepare_chroot_environment(thread)
    utilities.create_chroot_terminal(thread)

    is_chroot = utilities.check_chroot(thread)

    time.sleep(1.00)

    if is_chroot:
        # Connect terminal exit handler.
        terminal = model.builder.get_object('terminal_page__terminal')
        handler_id = terminal.connect(
            'child-exited',
            handlers.on_child_exited__terminal_page)
        model.set_handler_id(handler_id)
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are in the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are not in the chroot environment. Terminal input has been disabled.'
        )
        display.set_visible('terminal_page__exit_terminal_label', True)

    display.hide_spinner()
    utilities.initialize_chroot_environment(thread)
    display.reset_buttons(True, True, is_chroot)


def _transition__from__unsquashfs_page__to__options_page(thread):

    # Similar functions:
    # 1. _transition__from__unsquashfs_page__to__options_page
    # 2. transition__from__terminal_page__to__options_page

    _transition__from__unknown_page__to__options_page(
        'unsquashfs_page',
        thread)


#
# Terminal Page
#


def transition__from__terminal_page__to__options_page(thread):

    # Similar functions:
    # 1. _transition__from__unsquashfs_page__to__options_page
    # 2. transition__from__terminal_page__to__options_page

    _transition__from__unknown_page__to__options_page('terminal_page', thread)


def transition__from__terminal_page__to__copy_files_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Create a file details list of files to be copied.
    file_details_list = utilities.create_file_details_list()

    # [2] Prepare and display the new page.

    display.set_sensitive('copy_files_page__scrolled_window', False)
    display.reset_buttons(True, True, False)

    total_files = len(model.uris)
    current_directory = utilities.get_current_directory()
    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    relative_directory = os.path.join(
        '/',
        os.path.relpath(current_directory,
                        custom_squashfs_directory))

    if total_files == 1:
        label = 'Copy one file to %s' % relative_directory
    else:
        label = 'Copy %s files to %s' % (total_files, relative_directory)
    display.update_label('copy_files_page__progress_label', label)

    display.update_progressbar_text(
        'copy_files_page__copy_files_progressbar',
        None)
    display.update_progressbar_percent(
        'copy_files_page__copy_files_progressbar',
        0)
    display.update_liststore(
        'copy_files_page__file_details__liststore',
        file_details_list)

    # Transition to the Copy Files page.
    display.show_page('terminal_page', 'copy_files_page')
    display.set_sensitive('copy_files_page__scrolled_window', True)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()
    display.reset_buttons(
        True,
        True,
        True,
        back_button_label='Cancel',
        next_button_label='Copy')


#
# Copy Files Page
#

# TODO: Consider converting to (page, function) instead of (page, page)
# For example,...
# (1) transition__from__copy_files_page__to__terminal_page_copy_files()
#     - Copy files first, then automatically transition to terminal page.
# (2) transition__from__copy_files_page__to__terminal_page_cancel_copy_files()
#     - Do not Copy files; automatically transition to terminal page.


def transition__from__copy_files_page__to__terminal_page_copy_files(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.reset_buttons(True, True, False)

    # Copy the files.
    utilities.copy_files(thread)

    display.reset_buttons()

    # Pause to let the user read the screen before automatic transition.
    time.sleep(1.0)
    display.show_spinner()

    # [2] Prepare and display the new page.

    # display.update_label(
    #     'terminal_page__exit_terminal_label',
    #     'You have exited from the chroot environment. Click the Back button to re-enter.')
    # display.set_visible('terminal_page__exit_terminal_label', False)

    # Transition to the Copy Files page.
    display.show_page('copy_files_page', 'terminal_page')
    display.reset_buttons(True, True, True)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


#
# Options Page
#


def transition__from__options_page__to__repackage_iso_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Update filesystem.manifest-remove file.
    # filename = 'filesystem.manifest-remove'
    # is_exists = utilities.is_exists_filesystem_manifest_remove(filename)
    # removable_packages_list = utilities.create_typical_removable_packages_list(
    # )
    # Save the filesystem.manifest-remove file if there are packages to remove
    # or if the file already exists.
    # if is_exists or removable_packages_list:
    #     # This function will create the file if it does not exist.
    #     utilities.create_filesystem_manifest_remove_file(
    #         filename,
    #         removable_packages_list)

    # Update filesystem.manifest-remove file.
    # Always save the filesystem.manifest-remove file, even if there are no
    # packages to remove. If the does not exist an empty file will be created.
    # This function will create the file if it does not exist.
    filename = 'filesystem.manifest-remove'
    removable_packages_list = utilities.create_typical_removable_packages_list(
    )
    utilities.create_filesystem_manifest_remove_file(
        filename,
        removable_packages_list)

    # Update filesystem.manifest-minimal-remove file.
    filename = 'filesystem.manifest-minimal-remove'
    is_exists = utilities.is_exists_filesystem_manifest_remove(filename)
    removable_packages_list = utilities.create_minimal_removable_packages_list(
    )
    # Save the filesystem.manifest-minimal-remove file if there are packages to
    # remove or if the file already exists. If the file does not exist, there
    # will not be any packages to remove. (In the future, if we may show the
    # minimal remove column even when the file does not exist).
    if is_exists or removable_packages_list:
        # This function will create the file if it does not exist.
        utilities.create_filesystem_manifest_remove_file(
            filename,
            removable_packages_list)

    # Save preseed files.
    # TODO: Remove this line when 14.04 is no longer supported.
    # Bypass this functionality for Ubuntu 14.04.
    if model.builder.get_object('options_page__preseed_tab__stack'):
        logger.log_note('Save preseed files')
        utilities.save_stack_buffers('options_page__preseed_tab__stack')

    # Delete preseed files.
    if model.delete_list:
        logger.log_note('Delete preseed files')
        for filepath in model.delete_list:
            try:
                logger.log_data('Delete file', filepath)
                os.remove(filepath)
            except OSError as exception:
                logger.log_data('Error deleting file', exception)
        model.delete_list = []

    # Save ISO boot configurations.
    # TODO: Remove this line when 14.04 is no longer supported.
    # Bypass this functionality for Ubuntu 14.04.
    if model.builder.get_object('options_page__boot_configuration_tab__stack'):
        logger.log_note('Save ISO boot configurations')
        utilities.save_stack_buffers(
            'options_page__boot_configuration_tab__stack')
    else:
        utilities.update_and_save_boot_configurations()

    # [2] Prepare and display the new page.

    display.update_progressbar_percent(
        'repackage_iso_page__copy_boot_files_progressbar',
        0)
    display.update_progressbar_text(
        'repackage_iso_page__copy_boot_files_progressbar',
        '')
    display.update_progressbar_percent(
        'repackage_iso_page__create_squashfs_progressbar',
        0)
    display.update_progressbar_text(
        'repackage_iso_page__create_squashfs_progressbar',
        '')
    display.update_progressbar_percent(
        'repackage_iso_page__create_iso_image_progressbar',
        0)
    display.update_progressbar_text(
        'repackage_iso_page__create_iso_image_progressbar',
        '')

    display.update_label(
        'repackage_iso_page__update_filesystem_size_result_label',
        '...')
    display.update_label(
        'repackage_iso_page__update_disk_name_result_label',
        '...')
    display.update_progressbar_percent(
        'repackage_iso_page__update_checksums_progressbar',
        0)
    display.update_progressbar_text(
        'repackage_iso_page__update_checksums_progressbar',
        '')
    display.set_label_error(
        'repackage_iso_page__check_iso_size_result_label',
        False)
    display.update_label(
        'repackage_iso_page__check_iso_size_result_label',
        '...')
    display.update_label(
        'repackage_iso_page__calculate_iso_image_md5_sum_result_label',
        '...')
    display.update_label(
        'repackage_iso_page__calculate_iso_image_md5_filename_result_label',
        '...')
    display.update_status(
        'repackage_iso_page__copy_boot_files',
        display.BULLET)
    display.update_status(
        'repackage_iso_page__create_squashfs',
        display.BULLET)
    display.update_status(
        'repackage_iso_page__update_filesystem_size',
        display.BULLET)
    display.update_status(
        'repackage_iso_page__update_disk_name',
        display.BULLET)
    display.update_status(
        'repackage_iso_page__update_checksums',
        display.BULLET)
    display.update_status('repackage_iso_page__check_iso_size', display.BULLET)
    display.update_status(
        'repackage_iso_page__create_iso_image',
        display.BULLET)
    display.update_status(
        'repackage_iso_page__calculate_iso_image_md5_sum',
        display.BULLET)

    # Transition to the Repackage ISO page.
    display.show_page('options_page', 'repackage_iso_page')
    display.reset_buttons(True, True, False, next_button_label='Finish')

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()

    # Copy boot files.
    display.update_status(
        'repackage_iso_page__copy_boot_files',
        display.PROCESSING)
    time.sleep(0.25)
    utilities.copy_vmlinuz_and_initrd_files(thread)
    display.update_status('repackage_iso_page__copy_boot_files', display.OK)
    time.sleep(1.00)

    # Create squashfs.
    display.update_status(
        'repackage_iso_page__create_squashfs',
        display.PROCESSING)
    time.sleep(0.25)
    utilities.create_squashfs(thread)
    display.update_status('repackage_iso_page__create_squashfs', display.OK)
    time.sleep(1.00)

    # Update filesystem size.
    display.update_status(
        'repackage_iso_page__update_filesystem_size',
        display.PROCESSING)
    time.sleep(0.25)
    filesystem_size = utilities.update_filesystem_size(thread)
    logger.log_data(
        'The file system size is',
        '%.2f GiB (%s bytes)' %
        ((filesystem_size / 1073741824.0),
         filesystem_size))
    display.update_label(
        'repackage_iso_page__update_filesystem_size_result_label',
        'The file system size is %.2f GiB (%s bytes).' %
        ((filesystem_size / 1073741824.0),
         filesystem_size))
    display.update_status(
        'repackage_iso_page__update_filesystem_size',
        display.OK)
    time.sleep(1.00)

    # Update disk name.
    display.update_status(
        'repackage_iso_page__update_disk_name',
        display.PROCESSING)
    time.sleep(0.25)
    utilities.update_disk_name()
    utilities.update_disk_info()
    logger.log_data('Updated the disk name', model.custom_iso_image_disk_name)
    display.update_label(
        'repackage_iso_page__update_disk_name_result_label',
        'The disk name is %s.' % model.custom_iso_image_disk_name)
    display.update_status('repackage_iso_page__update_disk_name', display.OK)
    time.sleep(1.00)

    # Update MD5 sums.
    display.update_status(
        'repackage_iso_page__update_checksums',
        display.PROCESSING)
    time.sleep(0.25)
    checksums_filepath = os.path.join(
        model.custom_live_iso_directory,
        'md5sum.txt')
    exclude_paths = [
        os.path.join(model.custom_live_iso_directory,
                     'isolinux'),
        checksums_filepath
    ]
    count = utilities.update_md5_checksums(
        checksums_filepath,
        model.custom_live_iso_directory,
        exclude_paths)
    # count = utilities.count_lines(checksums_filepath, thread)
    logger.log_data('Number of checksums calculated', count)
    display.update_progressbar_text(
        'repackage_iso_page__update_checksums_progressbar',
        'Calculated checksums for %i files' % count)
    display.update_status('repackage_iso_page__update_checksums', display.OK)
    time.sleep(1.00)

    # Check ISO size and create ISO image.
    display.update_status(
        'repackage_iso_page__check_iso_size',
        display.PROCESSING)
    time.sleep(0.25)
    directory_size_bytes = utilities.get_directory_size(
        model.custom_live_iso_directory)
    directory_size_gib = directory_size_bytes / 1073741824.0
    logger.log_data(
        'The total size of all files on the disk is',
        '%.2f GiB (%i bytes)' % (directory_size_gib,
                                 directory_size_bytes))
    logger.log_data(
        'The maximum size limit for all files on the disk is',
        '%.2f GiB (%i bytes)' % (MAXIMUM_ISO_SIZE_GIB,
                                 MAXIMUM_ISO_SIZE_BYTES))
    # TODO: Add or improve log statments below.
    if directory_size_bytes > MAXIMUM_ISO_SIZE_BYTES:
        # Show directory size error message.
        display.update_status(
            'repackage_iso_page__check_iso_size',
            display.ERROR)
        display.set_label_error(
            'repackage_iso_page__check_iso_size_result_label',
            True)
        display.update_label(
            'repackage_iso_page__check_iso_size_result_label',
            'The total size of all files is %.2f GiB (%i bytes).' %
            (directory_size_gib,
             directory_size_bytes) + os.linesep +
            'This is larger than the %.2f GiB (%i bytes) limit.' %
            (MAXIMUM_ISO_SIZE_GIB,
             MAXIMUM_ISO_SIZE_BYTES) + os.linesep +
            'Click the Back button, and reduce the size of the Linux file system.'
        )
        logger.log_data(display.ERROR, 'Disk size exceeds maximum')
    else:
        # Show directory size.
        display.update_status('repackage_iso_page__check_iso_size', display.OK)
        display.set_label_error(
            'repackage_iso_page__check_iso_size_result_label',
            False)
        display.update_label(
            'repackage_iso_page__check_iso_size_result_label',
            'The total size of all files is %.2f GiB (%i bytes).' %
            (directory_size_gib,
             directory_size_bytes))

        # Create ISO image.
        display.update_status(
            'repackage_iso_page__create_iso_image',
            display.PROCESSING)
        time.sleep(0.25)
        utilities.create_iso_image(thread)
        display.update_status(
            'repackage_iso_page__create_iso_image',
            display.OK)
        time.sleep(1.00)

        # Calculate ISO image MD5 checksum.
        display.update_status(
            'repackage_iso_page__calculate_iso_image_md5_sum',
            display.PROCESSING)
        time.sleep(0.25)
        utilities.calculate_md5_hash_for_iso()
        display.update_label(
            'repackage_iso_page__calculate_iso_image_md5_sum_result_label',
            'The MD5 checksum is %s.' % model.custom_iso_image_md5_sum)
        display.update_label(
            'repackage_iso_page__calculate_iso_image_md5_filename_result_label',
            'The MD5 checksum file is %s.' %
            model.custom_iso_image_md5_filename)
        display.update_status(
            'repackage_iso_page__calculate_iso_image_md5_sum',
            display.OK)
        time.sleep(0.25)

        display.reset_buttons(True, True, True, next_button_label='Finish')


#
# Repackage ISO Page
#


def transition__from__repackage_iso_page__to__finish_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons(False, False, False, next_button_label='Close')

    # [2] Prepare and display the new page.

    # Display custom values.
    display.update_entry(
        'finish_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'finish_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'finish_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'finish_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'finish_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'finish_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)
    display.update_entry(
        'finish_page__custom_iso_image_md5_entry',
        model.custom_iso_image_md5_sum)
    display.update_entry(
        'finish_page__custom_iso_image_md5_filename_entry',
        model.custom_iso_image_md5_filename)

    # Transition to the Finish page.
    display.show_page('repackage_iso_page', 'finish_page')
    display.reset_buttons(False, False, True, next_button_label='Close')

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


########################################################################
# TransitionThread - Transition "Back" Functions
########################################################################


def transition__from__new_project_page__to__project_directory_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # [2] Prepare and display the new page.

    # model.set_project_directory('')
    # display.update_entry('project_directory_page__project_directory_entry', project_directory)

    # Transition to the Project Directory page.
    display.show_page('new_project_page', 'project_directory_page')
    display.reset_buttons(True, False, True)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


def transition__from__existing_project_page__to__project_directory_page(
        thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # [2] Prepare and display the new page.

    # model.set_project_directory('')
    # display.update_entry('project_directory_page__project_directory_entry', project_directory)

    # Transition to the Project Directory page.
    display.show_page('existing_project_page', 'project_directory_page')
    display.reset_buttons(True, False, True)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


def transition__from__delete_project_page__to__existing_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    display.set_sensitive(
        'existing_project_page__original_iso_image_filepath_filechooser__open_button',
        False)

    validators.validate_existing_project_page_for_delete()

    # [2] Prepare and display the new page.

    # Transition to the Existing Project page.
    display.show_page('delete_project_page', 'existing_project_page')
    display.reset_buttons(True, True, True)

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


def transition__from__unsquashfs_page__to__existing_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)

    display.show_spinner()
    display.reset_buttons()

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'existing_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'existing_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'existing_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'existing_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'existing_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'existing_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'existing_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'existing_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # Transition to the Existing Project page.
    display.show_page('unsquashfs_page', 'existing_project_page')
    display.reset_buttons(True, True, True)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page()

    display.hide_spinner()

    model.set_propagate(True)


def transition__from__terminal_page__to__existing_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    model.set_propagate(False)

    display.show_spinner()
    display.reset_buttons()

    # Exit the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Exiting from the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    # Disconnect terminal exit handler.
    if model.handler_id:
        terminal = model.builder.get_object('terminal_page__terminal')
        terminal.disconnect(model.handler_id)
        model.set_handler_id(None)

    utilities.exit_chroot_environment(thread)

    is_chroot = utilities.check_chroot(thread)

    if not is_chroot:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Successfully exited from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Unable to exit from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)

    time.sleep(1.00)

    # [2] Prepare and display the new page.

    # Display original values.
    display.update_entry(
        'existing_project_page__original_iso_image_filename_entry',
        model.original_iso_image_filename)
    display.update_entry(
        'existing_project_page__original_iso_image_directory_entry',
        model.original_iso_image_directory)
    display.update_entry(
        'existing_project_page__original_iso_image_volume_id_entry',
        model.original_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__original_iso_image_release_name_entry',
        model.original_iso_image_release_name)
    display.update_entry(
        'existing_project_page__original_iso_image_disk_name_entry',
        model.original_iso_image_disk_name)

    # Display custom values.
    display.update_entry(
        'existing_project_page__custom_iso_image_version_number_entry',
        model.custom_iso_image_version_number)
    display.update_entry(
        'existing_project_page__custom_iso_image_filename_entry',
        model.custom_iso_image_filename)
    display.update_entry(
        'existing_project_page__custom_iso_image_directory_entry',
        model.custom_iso_image_directory)
    display.update_entry(
        'existing_project_page__custom_iso_image_volume_id_entry',
        model.custom_iso_image_volume_id)
    display.update_entry(
        'existing_project_page__custom_iso_image_release_name_entry',
        model.custom_iso_image_release_name)
    display.update_entry(
        'existing_project_page__custom_iso_image_disk_name_entry',
        model.custom_iso_image_disk_name)

    # Transition to the Existing Project page.
    display.show_page('terminal_page', 'existing_project_page')
    display.reset_buttons(True, True, True)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page()

    display.hide_spinner()

    model.set_propagate(True)


def transition__from__copy_files_page__to__terminal_page_cancel_copy_files(
        thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    # [2] Prepare and display the new page.

    transition('copy_files_page', 'terminal_page', True, True, True)

    # [3] Perform functions on the new page, and activate the new page.


def transition__from__options_page__to__terminal_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # [2] Prepare and display the new page.

    # display.set_label_error('terminal_page__exit_terminal_label', False)
    # display.update_label(
    #     'terminal_page__exit_terminal_label',
    #     '...')
    # display.set_visible('terminal_page__exit_terminal_label', True)

    # Transition to the Terminal page.
    display.show_page('options_page', 'terminal_page')

    # [3] Perform functions on the new page, and activate the new page.

    # Enter the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Entering the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    utilities.prepare_chroot_environment(thread)
    utilities.create_chroot_terminal(thread)

    is_chroot = utilities.check_chroot(thread)

    time.sleep(1.00)

    if is_chroot:
        # Connect terminal exit handler.
        terminal = model.builder.get_object('terminal_page__terminal')
        handler_id = terminal.connect(
            'child-exited',
            handlers.on_child_exited__terminal_page)
        model.set_handler_id(handler_id)
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are in the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are not in the chroot environment. Terminal input has been disabled.'
        )
        display.set_visible('terminal_page__exit_terminal_label', True)

    display.hide_spinner()
    utilities.initialize_chroot_environment(thread)
    display.reset_buttons(True, True, is_chroot)


def transition__from__options_page__to__existing_project_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    # [2] Prepare and display the new page.

    transition('options_page', 'existing_project_page', True, True, True)

    # [3] Perform functions on the new page, and activate the new page.

    validators.validate_existing_project_page()


def transition__from__repackage_iso_page__to__options_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # [2] Prepare and display the new page.

    # Transition to the Manage Options.
    display.show_page('repackage_iso_page', 'options_page')
    display.reset_buttons(True, True, True, next_button_label='Generate')

    # [3] Perform functions on the new page, and activate the new page.

    display.hide_spinner()


########################################################################
# TransitionThread - Transition "Exit" Functions
########################################################################


def transition__from__project_directory_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__new_project_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__existing_project_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__delete_project_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__unsquashfs_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount the original ISO image and delete the mount point.
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__terminal_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount and delete directory (original-iso-mount).
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # Exit the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Exiting from the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    # Disconnect terminal exit handler.
    if model.handler_id:
        terminal = model.builder.get_object('terminal_page__terminal')
        terminal.disconnect(model.handler_id)
        model.set_handler_id(None)

    utilities.exit_chroot_environment(thread)

    is_chroot = utilities.check_chroot(thread)

    if not is_chroot:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Successfully exited from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Unable to exit from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)

    time.sleep(1.00)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__terminal_page__to__terminal_page(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons(True, True, False)

    # Unmount and delete directory (original-iso-mount).
    # logger.log_data('Unmount and delete the original ISO image mount point', model.original_iso_image_mount_point)
    # utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # [2] Prepare and display the new page.

    # display.set_label_error('terminal_page__exit_terminal_label', False)
    # display.update_label(
    #     'terminal_page__exit_terminal_label',
    #     '...')
    # display.set_visible('terminal_page__exit_terminal_label', True)

    # Transition to the Terminal page.
    # display.show_page('unsquashfs_page', 'terminal_page')

    # [3] Perform functions on the new page, and activate the new page.

    # Exit the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Exiting from the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    # Disconnect terminal exit handler.
    if model.handler_id:
        terminal = model.builder.get_object('terminal_page__terminal')
        terminal.disconnect(model.handler_id)
        model.set_handler_id(None)

    utilities.exit_chroot_environment(thread)

    is_chroot = utilities.check_chroot(thread)

    if not is_chroot:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Successfully exited from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Unable to exit from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)

    time.sleep(0.25)

    # Enter the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Reentering the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    utilities.prepare_chroot_environment(thread)
    utilities.create_chroot_terminal(thread)

    is_chroot = utilities.check_chroot(thread)

    time.sleep(1.00)

    if is_chroot:
        # Connect terminal exit handler.
        terminal = model.builder.get_object('terminal_page__terminal')
        handler_id = terminal.connect(
            'child-exited',
            handlers.on_child_exited__terminal_page)
        model.set_handler_id(handler_id)
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are in the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'You are not in the chroot environment. Terminal input has been disabled.'
        )
        display.set_visible('terminal_page__exit_terminal_label', True)

    display.hide_spinner()
    utilities.initialize_chroot_environment(thread)
    display.reset_buttons(True, True, is_chroot)


def transition__from__copy_files_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    # This is the same as exiting the terminal page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount and delete directory (original-iso-mount).
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # Exit the chroot environment.

    display.set_label_error('terminal_page__exit_terminal_label', False)
    display.update_label(
        'terminal_page__exit_terminal_label',
        'Exiting from the chroot environment...')
    display.set_visible('terminal_page__exit_terminal_label', True)

    # Disconnect terminal exit handler.
    if model.handler_id:
        terminal = model.builder.get_object('terminal_page__terminal')
        terminal.disconnect(model.handler_id)
        model.set_handler_id(None)

    utilities.exit_chroot_environment(thread)

    is_chroot = utilities.check_chroot(thread)

    ### TODO: This is not needed because we are not on the terminal page.
    if not is_chroot:
        # Disable input to the terminal.
        display.set_sensitive('terminal_page__terminal', False)
        display.set_label_error('terminal_page__exit_terminal_label', False)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Successfully exited from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)
    else:
        # Enable input to the terminal.
        display.set_sensitive('terminal_page__terminal', True)
        display.set_label_error('terminal_page__exit_terminal_label', True)
        display.update_label(
            'terminal_page__exit_terminal_label',
            'Unable to exit from the chroot environment.')
        display.set_visible('terminal_page__exit_terminal_label', True)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__options_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount and delete directory (original-iso-mount).
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__repackage_iso_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons()

    # Unmount and delete directory (original-iso-mount).
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # Delete the custom live ISO directory (custom-live-iso) because it may be corrupt.
    # TODO: It may be more efficient to check if everything completed successfully.
    #       If so, no need to delete this.
    #       Technically, you could leave this, because it will get overwritten, next time.
    # logger.log_data('Delete the custom live ISO directory', model.custom_live_iso_directory)
    # utilities.delete_file(model.custom_live_iso_directory, thread)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')


def transition__from__finish_page__to__exit(thread):

    # [1] Perform functions on the current page, and deactivate the current page.

    display.show_spinner()
    display.reset_buttons(False, False, False, next_button_label='Close')

    # Unmount and delete directory (original-iso-mount).
    logger.log_data(
        'Unmount and delete the original ISO image mount point',
        model.original_iso_image_mount_point)
    utilities.delete_iso_mount(model.original_iso_image_mount_point, thread)

    # Delete project files, if requested.
    checkbutton = model.builder.get_object(
        'finish_page__delete_project_files_checkbutton')
    is_active = checkbutton.get_active()
    logger.log_data(
        'The delete project files checkbutton is checked?',
        is_active)
    if is_active:
        # Delete directory: custom-live-iso
        logger.log_data(
            'Delete the custom live ISO directory',
            model.custom_live_iso_directory)
        utilities.delete_file(model.custom_live_iso_directory, thread)

        # Delete file: cubic.conf
        logger.log_data(
            'Delete the configuration file',
            model.configuration_filepath)
        utilities.delete_file(model.configuration_filepath, thread)

        # Delete directory: squashfs-root
        logger.log_data(
            'Delete the custom squashfs directory',
            model.custom_squashfs_directory)
        utilities.delete_file(model.custom_squashfs_directory, thread)

        # Delete directory: project directory
        # Do not delete this directory because it may be used for other purposes.
        # logger.log_data('Delete the project directory', model.project_directory)
        # try:
        #     os.rmdir(model.project_directory)
        # except OSError as exception:
        #     logger.log_data('The directory could not be deleted due to', exception)

    display.main_quit()
    display.hide_spinner()

    # [2] Prepare and display the new page.

    # [3] Perform functions on the new page, and activate the new page.

    logger.log_data('Exiting', 'Finished')
