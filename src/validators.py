#!/usr/bin/python3

########################################################################
#                                                                      #
# validators.py                                                        #
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
import logger
import model
import utilities


def validate_project_directory_page():

    is_page_complete = (bool(model.project_directory.strip()))

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', is_page_complete)

    logger.log_data(
        'Is project directory page, original section, valid?',
        is_page_complete)


# TODO: This function is not used.
def validate_new_project_page_original():

    is_page_complete = True

    # Original Iso Image Filename
    is_field_complete = (
        bool(model.original_iso_image_filename.strip())
        and utilities.is_mounted(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point))
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_filename',
        status)

    # Original Iso Image Directory
    is_field_complete = bool(model.original_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_directory',
        status)

    # Original Iso Image Volume Id
    is_field_complete = bool(model.original_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_volume_id',
        status)

    # Original Iso Image Release Name
    is_field_complete = bool(model.original_iso_image_release_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_release_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_release_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_release_name',
        status)

    # Original Iso Image Disk Name
    is_field_complete = bool(model.original_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_entry_editable(
        'new_project_page__custom_iso_image_version_number_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_filename_entry',
        is_page_complete)
    # display.set_entry_editable(
    #     'new_project_page__custom_iso_image_directory_entry',
    #     is_page_complete)
    display.set_sensitive(
        'new_project_page__custom_iso_image_directory_filechooser__open_button',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_volume_id_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_release_name_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_disk_name_entry',
        is_page_complete)

    logger.log_data(
        'Is new project page, original section, valid?',
        is_page_complete)


def validate_new_project_page_custom():

    is_page_complete = True

    # Custom Iso Image Version Number (Optional)
    is_field_complete = bool(model.custom_iso_image_version_number.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'new_project_page__custom_iso_image_version_number_label',
    #      not is_field_complete)
    # display.set_entry_error(
    #     'new_project_page__custom_iso_image_version_number_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'new_project_page__custom_iso_image_version_number',
        status)

    # Custom Iso Image Filename
    is_field_complete = bool(
        model.custom_iso_image_filename.strip()
        and model.custom_iso_image_filename.strip()[0] != '.')
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_filename',
        status)

    # Custom Iso Image Directory
    is_field_complete = bool(model.custom_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_directory',
        status)

    # Custom Iso Image Volume Id
    is_field_complete = bool(model.custom_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_volume_id',
        status)

    # Custom Iso Image Release Name (Optional)
    is_field_complete = bool(model.custom_iso_image_release_name.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'new_project_page__custom_iso_image_release_name_label',
    #      not is_field_complete)
    # display.set_entry_error(
    #     'new_project_page__custom_iso_image_release_name_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'new_project_page__custom_iso_image_release_name',
        status)

    # Custom Iso Image Disk Name
    is_field_complete = bool(model.custom_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', is_page_complete)

    logger.log_data(
        'Is new project page, custom section, valid?',
        is_page_complete)


def validate_new_project_page():

    is_page_complete = True

    #
    # Validate new project page, original section.
    #

    # Original Iso Image Filename
    is_field_complete = (
        bool(model.original_iso_image_filename.strip())
        and utilities.is_mounted(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point))
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_filename',
        status)

    # Original Iso Image Directory
    is_field_complete = bool(model.original_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_directory',
        status)

    # Original Iso Image Volume Id
    is_field_complete = bool(model.original_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_volume_id',
        status)

    # Original Iso Image Release Name
    is_field_complete = bool(model.original_iso_image_release_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_release_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_release_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_release_name',
        status)

    # Original Iso Image Disk Name
    is_field_complete = bool(model.original_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__original_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__original_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__original_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_entry_editable(
        'new_project_page__custom_iso_image_version_number_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_filename_entry',
        is_page_complete)
    # display.set_entry_editable(
    #     'new_project_page__custom_iso_image_directory_entry',
    #     is_page_complete)
    display.set_sensitive(
        'new_project_page__custom_iso_image_directory_filechooser__open_button',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_volume_id_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_release_name_entry',
        is_page_complete)
    display.set_entry_editable(
        'new_project_page__custom_iso_image_disk_name_entry',
        is_page_complete)

    logger.log_data(
        'Is new project page, original section, valid?',
        is_page_complete)

    #
    # Validate new project page, custom section.
    #

    # Custom Iso Image Version Number (Optional)
    is_field_complete = bool(model.custom_iso_image_version_number.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'new_project_page__custom_iso_image_version_number_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'new_project_page__custom_iso_image_version_number_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'new_project_page__custom_iso_image_version_number',
        status)

    # Custom Iso Image Filename
    is_field_complete = bool(
        model.custom_iso_image_filename.strip()
        and model.custom_iso_image_filename.strip()[0] != '.')
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_filename',
        status)

    # Custom Iso Image Directory
    is_field_complete = bool(model.custom_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_directory',
        status)

    # Custom Iso Image Volume Id
    is_field_complete = bool(model.custom_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_volume_id',
        status)

    # Custom Iso Image Release Name (Optional)
    is_field_complete = bool(model.custom_iso_image_release_name.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'new_project_page__custom_iso_image_release_name_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'new_project_page__custom_iso_image_release_name_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'new_project_page__custom_iso_image_release_name',
        status)

    # Custom Iso Image Disk Name
    is_field_complete = bool(model.custom_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'new_project_page__custom_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'new_project_page__custom_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'new_project_page__custom_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', is_page_complete)

    logger.log_data(
        'Is new project page, custom section, valid?',
        is_page_complete)


# TODO: This function is not used.
def validate_existing_project_page_original():

    is_page_complete = True

    # Original Iso Image Filename
    is_field_complete = (
        bool(model.original_iso_image_filename.strip())
        and utilities.is_mounted(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point))
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_filename',
        status)

    # Original Iso Image Directory
    is_field_complete = bool(model.original_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_directory',
        status)

    # Original Iso Image Volume Id
    is_field_complete = bool(model.original_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_volume_id',
        status)

    # Original Iso Image Release Name
    is_field_complete = bool(model.original_iso_image_release_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_release_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_release_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_release_name',
        status)

    # Original Iso Image Disk Name
    is_field_complete = bool(model.original_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_entry_editable(
        'existing_project_page__custom_iso_image_version_number_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_filename_entry',
        is_page_complete)
    # display.set_entry_editable(
    #     'existing_project_page__custom_iso_image_directory_entry',
    #     is_page_complete)
    display.set_sensitive(
        'existing_project_page__custom_iso_image_directory_filechooser__open_button',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_volume_id_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_release_name_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_disk_name_entry',
        is_page_complete)

    logger.log_data(
        'Is existing project page, original section, valid?',
        is_page_complete)


def validate_existing_project_page_custom():

    is_page_complete = True

    # Custom Iso Image Version Number (Optional)
    is_field_complete = bool(model.custom_iso_image_version_number.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_version_number_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_version_number_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_version_number',
        status)

    # Custom Iso Image Filename
    is_field_complete = bool(
        model.custom_iso_image_filename.strip()
        and model.custom_iso_image_filename.strip()[0] != '.')
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_filename',
        status)

    # Custom Iso Image Directory
    is_field_complete = bool(model.custom_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_directory',
        status)

    # Custom Iso Image Volume Id
    is_field_complete = bool(model.custom_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_volume_id',
        status)

    # Custom Iso Image Release Name (Optional)
    is_field_complete = bool(model.custom_iso_image_release_name.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_release_name_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_release_name_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_release_name',
        status)

    # Custom Iso Image Disk Name
    is_field_complete = bool(model.custom_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', is_page_complete)

    logger.log_data(
        'Is existing project page, custom section, valid?',
        is_page_complete)


def validate_existing_project_page():

    is_page_complete = True

    #
    # Validate existing project page, original section.
    #

    # Original Iso Image Filename
    is_field_complete = (
        bool(model.original_iso_image_filename.strip())
        and utilities.is_mounted(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point))
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_filename',
        status)

    # Original Iso Image Directory
    is_field_complete = bool(model.original_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_directory',
        status)

    # Original Iso Image Volume Id
    is_field_complete = bool(model.original_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_volume_id',
        status)

    # Original Iso Image Release Name
    is_field_complete = bool(model.original_iso_image_release_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_release_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_release_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_release_name',
        status)

    # Original Iso Image Disk Name
    is_field_complete = bool(model.original_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_entry_editable(
        'existing_project_page__custom_iso_image_version_number_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_filename_entry',
        is_page_complete)
    # display.set_entry_editable(
    #     'existing_project_page__custom_iso_image_directory_entry',
    #     is_page_complete)
    display.set_sensitive(
        'existing_project_page__custom_iso_image_directory_filechooser__open_button',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_volume_id_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_release_name_entry',
        is_page_complete)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_disk_name_entry',
        is_page_complete)

    logger.log_data(
        'Is existing project page, original section, valid?',
        is_page_complete)

    #
    # Validate existing project page, custom section.
    #

    # Custom Iso Image Version Number (Optional)
    is_field_complete = bool(model.custom_iso_image_version_number.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_version_number_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_version_number_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_version_number',
        status)

    # Custom Iso Image Filename
    is_field_complete = bool(
        model.custom_iso_image_filename.strip()
        and model.custom_iso_image_filename.strip()[0] != '.')
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_filename',
        status)

    # Custom Iso Image Directory
    is_field_complete = bool(model.custom_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_directory',
        status)

    # Custom Iso Image Volume Id
    is_field_complete = bool(model.custom_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_volume_id',
        status)

    # Custom Iso Image Release Name (Optional)
    is_field_complete = bool(model.custom_iso_image_release_name.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_release_name_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_release_name_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_release_name',
        status)

    # Custom Iso Image Disk Name
    is_field_complete = bool(model.custom_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', is_page_complete)

    logger.log_data(
        'Is existing project page, custom section, valid?',
        is_page_complete)


def validate_existing_project_page_for_delete():

    is_page_complete = True

    #
    # Validate existing project page, original section.
    #

    # Original Iso Image Filename
    is_field_complete = (
        bool(model.original_iso_image_filename.strip())
        and utilities.is_mounted(
            model.original_iso_image_filepath,
            model.original_iso_image_mount_point))
    is_page_complete = is_page_complete and is_field_complete

    display.set_label_error(
        'existing_project_page__original_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_filename',
        status)

    # Original Iso Image Directory
    is_field_complete = bool(model.original_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_directory',
        status)

    # Original Iso Image Volume Id
    is_field_complete = bool(model.original_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_volume_id',
        status)

    # Original Iso Image Release Name
    is_field_complete = bool(model.original_iso_image_release_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_release_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_release_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_release_name',
        status)

    # Original Iso Image Disk Name
    is_field_complete = bool(model.original_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__original_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__original_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__original_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_entry_editable(
        'existing_project_page__custom_iso_image_version_number_entry',
        False)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_filename_entry',
        False)
    # display.set_entry_editable(
    #     'existing_project_page__custom_iso_image_directory_entry',
    #     False)
    display.set_sensitive(
        'existing_project_page__custom_iso_image_directory_filechooser__open_button',
        False)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_volume_id_entry',
        False)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_release_name_entry',
        False)
    display.set_entry_editable(
        'existing_project_page__custom_iso_image_disk_name_entry',
        False)

    logger.log_data(
        'Is existing project page, original section, for delete valid?',
        is_page_complete)

    #
    # Validate existing project page, custom section.
    #

    # Custom Iso Image Version Number (Optional)
    is_field_complete = bool(model.custom_iso_image_version_number.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_version_number_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_version_number_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_version_number',
        status)

    # Custom Iso Image Filename
    is_field_complete = bool(
        model.custom_iso_image_filename.strip()
        and model.custom_iso_image_filename.strip()[0] != '.')
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_filename_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_filename_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_filename',
        status)

    # Custom Iso Image Directory
    is_field_complete = bool(model.custom_iso_image_directory.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_directory_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_directory_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_directory',
        status)

    # Custom Iso Image Volume Id
    is_field_complete = bool(model.custom_iso_image_volume_id.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_volume_id_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_volume_id_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_volume_id',
        status)

    # Custom Iso Image Release Name (Optional)
    is_field_complete = bool(model.custom_iso_image_release_name.strip())
    # is_page_complete = is_page_complete and is_field_complete
    # display.set_label_error(
    #     'existing_project_page__custom_iso_image_release_name_label',
    #     not is_field_complete)
    # display.set_entry_error(
    #     'existing_project_page__custom_iso_image_release_name_entry',
    #     not is_field_complete)
    status = display.OK if is_field_complete else display.OPTIONAL
    display.update_status(
        'existing_project_page__custom_iso_image_release_name',
        status)

    # Custom Iso Image Disk Name
    is_field_complete = bool(model.custom_iso_image_disk_name.strip())
    is_page_complete = is_page_complete and is_field_complete
    display.set_label_error(
        'existing_project_page__custom_iso_image_disk_name_label',
        not is_field_complete)
    display.set_entry_error(
        'existing_project_page__custom_iso_image_disk_name_entry',
        not is_field_complete)
    status = display.OK if is_field_complete else display.ERROR
    display.update_status(
        'existing_project_page__custom_iso_image_disk_name',
        status)

    #
    # Set fields sensitive/insensitive or editable/non-editable based on results.
    #

    display.set_sensitive('next_button', True)

    logger.log_data(
        'Is existing project page, custom section, for delete valid?',
        is_page_complete)
