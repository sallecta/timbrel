#!/usr/bin/python3

########################################################################
#                                                                      #
# model.py                                                             #
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

import timbrel_log
me='model.py'

import logger

########################################################################
# General
########################################################################

theme_style = None
default_icon_theme_search_path = None
cubic_version = None
terminal_pid = None
builder = None
root_user_id = None
root_group_id = None
user_name = None
user_id = None
group_id = None
password = None
home = None
uris = None
page_name = None
propagate = None
transition_thread = None
handler_id = None

########################################################################
# Project
########################################################################

project_directory = None
configuration_filepath = None
original_iso_image_mount_point = None
custom_squashfs_directory = None
custom_live_iso_directory = None

########################################################################
# Original
########################################################################

original_iso_image_filepath = None
original_iso_image_filename = None
original_iso_image_directory = None
original_iso_image_volume_id = None
original_iso_image_release_name = None
original_iso_image_disk_name = None

casper_relative_directory = None

########################################################################
# Custom
########################################################################

custom_iso_image_version_number = None
custom_iso_image_filepath = None
custom_iso_image_filename = None
custom_iso_image_directory = None
custom_iso_image_volume_id = None
custom_iso_image_release_name = None
custom_iso_image_disk_name = None

custom_iso_image_md5_sum = None
custom_iso_image_md5_filepath = None
custom_iso_image_md5_filename = None

########################################################################
# Status
########################################################################

is_success_copy_original_iso_files = None
is_success_extract_squashfs = None

########################################################################
# Options
########################################################################

undo_index = 0
undo_list = []
delete_list = []
# boot_configurations = 'boot/grub/grub.cfg,boot/grub/loopback.cfg,isolinux/isolinux.cfg,isolinux/txt.cfg'
boot_configurations = []

########################################################################
# General
########################################################################


def set_version(new_version):
    global version
    version = new_version
    timbrel_log.info(me,'The Timbrel version is', version)


# def set_theme_style(new_theme_style):
    # global theme_style
    # theme_style = new_theme_style
    # timbrel_log.info(me,'The theme style is', theme_style)


# def set_default_icon_theme_search_path(new_default_icon_theme_search_path):
    # global default_icon_theme_search_path
    # default_icon_theme_search_path = new_default_icon_theme_search_path
    # timbrel_log.info(me,
        # 'The default icon theme search path is',
        # default_icon_theme_search_path)


def set_cubic_version(new_cubic_version):
    global cubic_version
    cubic_version = new_cubic_version
    timbrel_log.info(me,'The Timbrel version is', cubic_version)


def set_terminal_pid(new_terminal_pid):
    global terminal_pid
    terminal_pid = new_terminal_pid
    timbrel_log.info(me,'The terminal pid is', terminal_pid)


def set_builder(new_builder):
    global builder
    builder = new_builder
    timbrel_log.info(me,'The builder is', builder)


def set_root_user_id(new_root_user_id):
    global root_user_id
    try:
        root_user_id = int(new_root_user_id)
    except TypeError:
        root_user_id = -1
    except ValueError:
        root_user_id = -1
    timbrel_log.info(me,'The root user id is', root_user_id)


def set_root_group_id(new_root_group_id):
    global root_group_id
    try:
        root_group_id = int(new_root_group_id)
    except TypeError:
        root_group_id = -1
    except ValueError:
        root_group_id = -1
    timbrel_log.info(me,'The root group id is', root_group_id)


def set_user_name(new_user_name):
    global user_name
    user_name = new_user_name.strip() if new_user_name else ''
    timbrel_log.info(me,'The user name is', user_name)


def set_user_id(new_user_id):
    global user_id
    try:
        user_id = int(new_user_id)
    except TypeError:
        user_id = -1
    except ValueError:
        user_id = -1
    timbrel_log.info(me,'The user id is', user_id)


def set_group_id(new_group_id):
    global group_id
    try:
        group_id = int(new_group_id)
    except TypeError:
        group_id = -1
    except ValueError:
        group_id = -1
    timbrel_log.info(me,'The group id is', group_id)


def set_password(new_password):
    global password
    password = new_password.strip() if new_password else ''
    timbrel_log.info(me,'The password is', password)


def set_home(new_home):
    global home
    home = new_home.strip() if new_home else ''
    timbrel_log.info(me,'The home directory is', home)


def set_uris(new_uris):
    global uris
    uris = new_uris
    timbrel_log.info(me,'The uris is', uris)


def set_page_name(new_page_name):
    global page_name
    page_name = new_page_name.strip() if new_page_name else ''
    timbrel_log.info(me,'The current page name is', page_name)


def set_propagate(new_propagate):
    global propagate
    propagate = new_propagate
    timbrel_log.info(me,
        'Propagate assigned values to calculate dependant values?',
        propagate)


def set_handler_id(new_handler_id):
    global handler_id
    handler_id = new_handler_id
    timbrel_log.info(me,'The handler id is', handler_id)


########################################################################
# Project
########################################################################


def set_project_directory(new_project_directory):
    global project_directory
    project_directory = new_project_directory.strip(
    ) if new_project_directory else ''
    timbrel_log.info(me,'The project directory is', project_directory)


def set_configuration_filepath(new_configuration_filepath):
    global configuration_filepath
    configuration_filepath = new_configuration_filepath.strip(
    ) if new_configuration_filepath else ''
    timbrel_log.info(me,'The configuration filepath is', configuration_filepath)


def set_original_iso_image_mount_point(new_original_iso_image_mount_point):
    global original_iso_image_mount_point
    original_iso_image_mount_point = new_original_iso_image_mount_point.strip(
    ) if new_original_iso_image_mount_point else ''
    timbrel_log.info(me,
        'The original ISO image mount point is',
        original_iso_image_mount_point)


def set_custom_squashfs_directory(new_custom_squashfs_directory):
    global custom_squashfs_directory
    custom_squashfs_directory = new_custom_squashfs_directory.strip(
    ) if new_custom_squashfs_directory else ''
    timbrel_log.info(me,
        'The custom squashfs directory is',
        custom_squashfs_directory)


def set_custom_live_iso_directory(new_custom_live_iso_directory):
    global custom_live_iso_directory
    custom_live_iso_directory = new_custom_live_iso_directory.strip(
    ) if new_custom_live_iso_directory else ''
    timbrel_log.info(me,
        'The custom live ISO directory is',
        custom_live_iso_directory)


########################################################################
# Original
########################################################################


def set_original_iso_image_filepath(new_original_iso_image_filepath):
    global original_iso_image_filepath
    original_iso_image_filepath = new_original_iso_image_filepath.strip(
    ) if new_original_iso_image_filepath else ''
    timbrel_log.info(me,
        'The original ISO image filepath is',
        original_iso_image_filepath)


def set_original_iso_image_filename(new_original_iso_image_filename):
    global original_iso_image_filename
    original_iso_image_filename = new_original_iso_image_filename.strip(
    ) if new_original_iso_image_filename else ''
    timbrel_log.info(me,
        'The original ISO image filename is',
        original_iso_image_filename)


def set_original_iso_image_directory(new_original_iso_image_directory):
    global original_iso_image_directory
    original_iso_image_directory = new_original_iso_image_directory.strip(
    ) if new_original_iso_image_directory else ''
    timbrel_log.info(me,
        'The original ISO image directory is',
        original_iso_image_directory)


def set_original_iso_image_volume_id(new_original_iso_image_volume_id):
    global original_iso_image_volume_id
    original_iso_image_volume_id = new_original_iso_image_volume_id.strip(
    ) if new_original_iso_image_volume_id else ''
    timbrel_log.info(me,
        'The original ISO image volume id is',
        original_iso_image_volume_id)


def set_original_iso_image_release_name(new_original_iso_image_release_name):
    global original_iso_image_release_name
    original_iso_image_release_name = new_original_iso_image_release_name.strip(
    ) if new_original_iso_image_release_name else ''
    timbrel_log.info(me,
        'The original ISO image release name is',
        original_iso_image_release_name)


def set_original_iso_image_disk_name(new_original_iso_image_disk_name):
    global original_iso_image_disk_name
    original_iso_image_disk_name = new_original_iso_image_disk_name.strip(
    ) if new_original_iso_image_disk_name else ''
    timbrel_log.info(me,
        'The original ISO image disk name is',
        original_iso_image_disk_name)


def set_casper_relative_directory(new_casper_relative_directory):
    global casper_relative_directory
    casper_relative_directory = new_casper_relative_directory.strip(
    ) if new_casper_relative_directory else ''
    timbrel_log.info(me,
        'The casper relative directory is',
        casper_relative_directory)


########################################################################
# Custom
########################################################################


def set_custom_iso_image_version_number(new_custom_iso_image_version_number):
    global custom_iso_image_version_number
    custom_iso_image_version_number = new_custom_iso_image_version_number.strip(
    ) if new_custom_iso_image_version_number else ''
    timbrel_log.info(me,
        'The custom ISO image version number is',
        custom_iso_image_version_number)


def set_custom_iso_image_filepath(new_custom_iso_image_filepath):
    global custom_iso_image_filepath
    custom_iso_image_filepath = new_custom_iso_image_filepath.strip(
    ) if new_custom_iso_image_filepath else ''
    timbrel_log.info(me,
        'The custom ISO image filepath is',
        custom_iso_image_filepath)


def set_custom_iso_image_filename(new_custom_iso_image_filename):
    global custom_iso_image_filename
    custom_iso_image_filename = new_custom_iso_image_filename.strip(
    ) if new_custom_iso_image_filename else ''
    timbrel_log.info(me,
        'The custom ISO image filename is',
        custom_iso_image_filename)


def set_custom_iso_image_directory(new_custom_iso_image_directory):
    global custom_iso_image_directory
    custom_iso_image_directory = new_custom_iso_image_directory.strip(
    ) if new_custom_iso_image_directory else ''
    timbrel_log.info(me,
        'The custom ISO image directory is',
        custom_iso_image_directory)


def set_custom_iso_image_volume_id(new_custom_iso_image_volume_id):
    global custom_iso_image_volume_id
    custom_iso_image_volume_id = new_custom_iso_image_volume_id.strip(
    ) if new_custom_iso_image_volume_id else ''
    timbrel_log.info(me,
        'The custom ISO image volume id is',
        custom_iso_image_volume_id)


def set_custom_iso_image_release_name(new_custom_iso_image_release_name):
    global custom_iso_image_release_name
    custom_iso_image_release_name = new_custom_iso_image_release_name.strip(
    ) if new_custom_iso_image_release_name else ''
    timbrel_log.info(me,
        'The custom ISO image release name is',
        custom_iso_image_release_name)


def set_custom_iso_image_disk_name(new_custom_iso_image_disk_name):
    global custom_iso_image_disk_name
    custom_iso_image_disk_name = new_custom_iso_image_disk_name.strip(
    ) if new_custom_iso_image_disk_name else ''
    timbrel_log.info(me,
        'The custom ISO image disk name is',
        custom_iso_image_disk_name)


def set_custom_iso_image_md5_sum(new_custom_iso_image_md5_sum):
    global custom_iso_image_md5_sum
    custom_iso_image_md5_sum = new_custom_iso_image_md5_sum.strip(
    ) if new_custom_iso_image_md5_sum else ''
    timbrel_log.info(me,
        'The custom ISO image md5 sum is',
        custom_iso_image_md5_sum)


def set_custom_iso_image_md5_filepath(new_custom_iso_image_md5_filepath):
    global custom_iso_image_md5_filepath
    custom_iso_image_md5_filepath = new_custom_iso_image_md5_filepath.strip(
    ) if new_custom_iso_image_md5_filepath else ''
    timbrel_log.info(me,
        'The custom ISO image md5 filepath is',
        custom_iso_image_md5_filepath)


def set_custom_iso_image_md5_filename(new_custom_iso_image_md5_filename):
    global custom_iso_image_md5_filename
    custom_iso_image_md5_filename = new_custom_iso_image_md5_filename.strip(
    ) if new_custom_iso_image_md5_filename else ''
    timbrel_log.info(me,
        'The custom ISO image md5 filename is',
        custom_iso_image_md5_filename)


########################################################################
# Status
########################################################################


def set_is_success_copy_original_iso_files(
        new_is_success_copy_original_iso_files):
    global is_success_copy_original_iso_files
    is_success_copy_original_iso_files = new_is_success_copy_original_iso_files
    timbrel_log.info(me,
        'Is success copy boot files',
        is_success_copy_original_iso_files)


def set_is_success_extract_squashfs(new_is_success_extract_squashfs):
    global is_success_extract_squashfs
    is_success_extract_squashfs = new_is_success_extract_squashfs
    timbrel_log.info(me,
        'Is success extract squashfs?',
        is_success_extract_squashfs)


########################################################################
# Status
########################################################################


# Set boot configurations as a list.
def set_boot_configurations(new_boot_configurations):
    global boot_configurations
    boot_configurations = new_boot_configurations
    timbrel_log.info(me,'Set boot configurations', boot_configurations)


# Set boot configurations as a string with comma separated values.
def set_boot_configurations_as_string(new_boot_configurations):
    global boot_configurations
    boot_configurations = [
        boot_configuration.strip(' ' + os.sep)
        for boot_configuration in new_boot_configurations.split(',')
    ] if new_boot_configurations else []


# Add a boot configuration.
def add_boot_configuration(new_boot_configuration):
    global boot_configurations
    boot_configuration = new_boot_configuration.strip(' ' + os.sep)
    timbrel_log.info(me,'Add boot configuration', boot_configuration)
    boot_configurations.append(boot_configuration)


# TODO: Add a function add boot configurations as a list.
# TODO: Add a function add boot configurations as a tuple.
# TODO: Add function to remove a single boot configuration.
