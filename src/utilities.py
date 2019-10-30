#!/usr/bin/python3

########################################################################
#                                                                      #
# utilities.py                                                         #
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
me='utilites.py'
import timbrel_log

import display
import logger
import model

import configparser
import datetime
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
# gi.require_version('GtkSource', '3.0')
try:
    gi.require_version('GtkSource', '4')
    timbrel_log.info(me,'Using GtkSource version', '4')
except ValueError:
    gi.require_version('GtkSource', '3.0')
    timbrel_log.info(me,'Using GtkSource version', '3.0')
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import Pango
try:
    gi.require_version('Vte', '2.91')
    # timbrel_log.info(me,'Using Vte version', '2.91')
except ValueError:
    gi.require_version('Vte', '2.90')
    # timbrel_log.info(me,'Using Vte version', '2.90')
from gi.repository.Vte import Terminal, PtyFlags
import glob
import hashlib
import os
import pexpect
import platform
import re
from shutil import copyfile, move
import signal
import stat
import string
import time
import traceback
from urllib.parse import urlparse, unquote
# import uuid

# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
BOLD_RED = '\033[1;31m'
BOLD_GREEN = '\033[1;32m'
BOLD_BLUE = '\033[1;34m'
BOLD_YELLOW = '\033[1;33;1m'
NORMAL = '\033[0m'

########################################################################
# Execute Functions
########################################################################

# https://pexpect.readthedocs.org/en/stable/api/pexpect.html#spawn-class
# Because spwan() is a byte interface, you must use
# process.read().decode().
# Because spwanu() is a string interface, process.read().decode() is not
# necessary.


def execute_synchronous(command, thread=None, working_directory=None):
    timbrel_log.info(me,'Execute synchronously', command)

    result = None
    error = 1
    try:
        # Using pexpect.split_command_line removes the spaces in the
        # command. This results in the error:
        # pexpect.exceptions.ExceptionPexpect: The command was not found or
        # was not executable.
        # command = pexpect.split_command_line(command)
        # For Pexpect Pexpect 3.x
        process = pexpect.spawnu(command, timeout=300, cwd=working_directory)
        # For Pexpect 4.0
        # process = pexpect.spawn(command, timeout=300, cwd=working_directory, encoding='UTF-8')
        if thread:
            thread.set_process(process)
            # logger.log_data('The process id is', thread.get_process_id())
        result = process.read()
        result = result.strip() if result else None
        error = process.exitstatus
    except pexpect.ExceptionPexpect as exception:
        logger.log_data('Exception while executing', command)
        logger.log_data('The tracekback is', traceback.format_exc())

    return result, error


def execute_asynchronous(command, thread=None, working_directory=None):
    logger.log_data('Execute asynchronously', command)

    try:
        # Using pexpect.split_command_line removes the spaces in the
        # command. This results in the error:
        # pexpect.exceptions.ExceptionPexpect: The command was not found or
        # was not executable.
        # command = pexpect.split_command_line(command)
        # For Pexpect Pexpect 3.x
        process = pexpect.spawnu(command, timeout=300, cwd=working_directory)
        # For Pexpect 4.0
        # process = pexpect.spawn(command, timeout=300, cwd=working_directory, encoding='UTF-8')
        if thread:
            thread.set_process(process)
            # logger.log_data('• The process id is', thread.get_process_id())
    except pexpect.ExceptionPexpect as exception:
        logger.log_data('Exception while executing', command)
        logger.log_data('The tracekback is', traceback.format_exc())


########################################################################
# File Functions
########################################################################


def replace_text_in_file(filepath, search_text, replacement_text):
    logger.log_data('Replace text in file', filepath)
    logger.log_data('Search text', search_text)
    logger.log_data('Replacement text', replacement_text)

    if not filepath:
        logger.log_data('Cannot replace text', 'File not specified')
        return

    if not os.path.exists(filepath):
        logger.log_data(
            'Cannot replace text',
            'File %s does not exist' % filepath)
        return

    if not search_text:
        logger.log_data('Cannot replace text', 'Search text not specified')
        return

    if not replacement_text:
        logger.log_data(
            'Cannot replace text',
            'Replacement text not specified')
        return

    with open(filepath, 'r+') as file:
        file_contents = file.read()
        file_contents = re.sub(search_text, replacement_text, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)


def delete_file(filepath, thread):
    logger.log_data('Delete file', filepath)

    # TODO: Can we use python functions? We need a way to cancel a delete,
    #       operation, and using an external process thread allows that.
    #       Can something similar be achieved using python functions?
    # try:
    #     os.remove(filename)
    # except OSError as exception:
    #     logger.log_data('%s does not exist' % filepath, 'Cannot delete')
    # except OSError as exception:
    #     logger.log_data('Error deleting file %s' % filepath, exception)
    # except Exception as exception:
    #     logger.log_data('Error deleting file %s' % filepath, exception)

    if os.path.exists(filepath):
        command = 'rm -rf "%s"' % filepath
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Error deleting file %s' % filepath, result)
    else:
        logger.log_data('%s does not exist' % filepath, 'Cannot delete')


def get_directory_size(start_path):
    logger.log_note('Calculate directory size')
    logger.log_data('The directory is', start_path)

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    # logger.log_data('Directory size is', total_size)

    return total_size


def get_directory_for_file(filename, start_path):
    logger.log_data('Get directory for %s in' % filename, start_path)

    directory = ''
    for dirpath, dirnames, filenames in os.walk(start_path):
        if filename in filenames: directory = dirpath

    if directory:
        logger.log_data('%s is in' % filename, directory)
    else:
        logger.log_data('%s is not in' % filename, directory)

    return directory


########################################################################
# Miscelaneous Functions
########################################################################


def set_user_and_group(user_id, group_id):
    logger.log_data('Change user and group to', '%s:%s' % (user_id, group_id))
    os.setgid(group_id)
    os.setuid(user_id)


def get_current_directory():

    # Vte 2.91 only...
    # Note: on libvte-2.90, this returns the Computer Name and
    # directory, so it does not work.
    # terminal = model.builder.get_object("terminal_page_terminal")
    # current_directory_uri = terminal.get_current_directory_uri()
    # current_directory = urlparse(current_directory_uri).path

    # Vte 2.90 or Vte 2.91..
    current_directory = os.readlink('/proc/%i/cwd' % model.terminal_pid)

    return current_directory


def get_package_version(package_name):
    command = 'dpkg-query --showformat="${Version}\n" --show "%s"' % package_name
    result, error = execute_synchronous(command)
    return result


########################################################################
# Configuration File Functions
########################################################################

# def get_list_from_configuration(section, ):


# TODO: Make creating the configuration object more efficient by storing
#       it in the model.
def save_configuration():
    logger.log_data('Save configuration')

    # Create the configuraton.
    configuration = configparser.ConfigParser(allow_no_value=True)
    configuration.optionxform = str

    # General
    configuration.add_section('General')
    configuration.set('General', 'cubic_version', model.cubic_version)
    configuration.set('General', 'project_directory', model.project_directory)

    # Original
    configuration.add_section('Original')
    # configuration.set('Original',
    #     'original_iso_image_filepath',
    #     model.original_iso_image_filepath)
    configuration.set(
        'Original',
        'original_iso_image_filename',
        model.original_iso_image_filename)
    configuration.set(
        'Original',
        'original_iso_image_directory',
        model.original_iso_image_directory)
    configuration.set(
        'Original',
        'original_iso_image_volume_id',
        model.original_iso_image_volume_id)
    configuration.set(
        'Original',
        'original_iso_image_release_name',
        model.original_iso_image_release_name)
    configuration.set(
        'Original',
        'original_iso_image_disk_name',
        model.original_iso_image_disk_name)

    # Custom
    configuration.add_section('Custom')
    configuration.set(
        'Custom',
        'custom_iso_image_version_number',
        model.custom_iso_image_version_number)
    # configuration.set('Custom',
    #     'custom_iso_image_filepath',
    #     model.custom_iso_image_filepath)
    configuration.set(
        'Custom',
        'custom_iso_image_filename',
        model.custom_iso_image_filename)
    configuration.set(
        'Custom',
        'custom_iso_image_directory',
        model.custom_iso_image_directory)
    configuration.set(
        'Custom',
        'custom_iso_image_volume_id',
        model.custom_iso_image_volume_id)
    configuration.set(
        'Custom',
        'custom_iso_image_release_name',
        model.custom_iso_image_release_name)
    configuration.set(
        'Custom',
        'custom_iso_image_disk_name',
        model.custom_iso_image_disk_name)
    configuration.set(
        'Custom',
        'custom_iso_image_md5_filename',
        model.custom_iso_image_md5_filename)

    # Status
    configuration.add_section('Status')
    configuration.set(
        'Status',
        'is_success_copy_original_iso_files',
        str(model.is_success_copy_original_iso_files))
    configuration.set(
        'Status',
        'is_success_extract_squashfs',
        str(model.is_success_extract_squashfs))

    # Options
    configuration.add_section('Options')
    boot_configurations_string = ','.join(
        boot_configuration.strip(' /')
        for boot_configuration in model.boot_configurations)
    configuration.set(
        'Options',
        'boot_configurations',
        boot_configurations_string)

    # Write the configuration file.
    configuration_filepath = os.path.realpath(model.configuration_filepath)
    with open(configuration_filepath, 'w') as configuration_file:
        configuration.write(configuration_file)

    os.chown(configuration_filepath, model.user_id, model.group_id)

    # Alternate syntax...
    # configuration_file = open(model.configuration_filepath, 'w')
    # with configuration_file: configuration.write(configuration_file)


def save_configuration_value(section, key, value):
    # Create the configuration.
    configuration = configparser.ConfigParser(allow_no_value=True)
    configuration.optionxform = str

    # Set the section, key, and value.
    configuration.add_section(section)

    if type(value) is str:
        configuration.set(section, key, value)
    elif type(value) is bool:
        configuration.set(section, key, str(value))
    elif type(value) is tuple:
        configuration.set(section, key, ','.join(value))
    elif type(value) is list:
        configuration.set(section, key, ','.join(value))
    else:
        configuration.set(section, key, value)

    # Write the configuration file.
    configuration_filepath = os.path.realpath(model.configuration_filepath)
    with open(configuration_filepath, 'w') as configuration_file:
        configuration.write(configuration_file)


########################################################################
# ISO Mount Functions
########################################################################


def is_mounted(iso_image_filepath, iso_image_mount_point):
    logger.log_note('Check if ISO image is mounted')

    iso_image_filepath = os.path.realpath(iso_image_filepath)
    iso_image_mount_point = os.path.realpath(iso_image_mount_point)
    logger.log_data('ISO image', iso_image_filepath)
    logger.log_data('Mount point', iso_image_mount_point)
    command = 'mount'
    result, error = execute_synchronous(command)
    mounted = False
    if not error:
        mount_information = re.search(
            r'%s\s*on\s*%s' %
            (re.escape(iso_image_filepath),
             re.escape(iso_image_mount_point)),
            result)
        mounted = bool(mount_information)
    logger.log_data('Is mounted?', mounted)
    return mounted


def mount_iso_image(iso_image_filepath, iso_image_mount_point, thread):
    logger.log_note('Mount ISO image')

    iso_image_filepath = os.path.realpath(iso_image_filepath)
    iso_image_mount_point = os.path.realpath(iso_image_mount_point)
    logger.log_data('ISO image', iso_image_filepath)
    logger.log_data('Mount point', iso_image_mount_point)

    if os.path.exists(iso_image_mount_point):
        # Unmount existing mount point, just in case it is already
        # mounted.
        logger.log_data(
            'Unmount existing mount point if it is mounted',
            iso_image_mount_point)
        command = 'umount "%s"' % iso_image_mount_point
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Unable to unmount', result)
    else:
        # Create the mount point if it does not exist.
        logger.log_data(
            'Create the mount point if it does not exist',
            iso_image_mount_point)
        command = 'mkdir "%s"' % iso_image_mount_point
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Unable to create the mount point', result)

    if os.path.exists(iso_image_filepath):
        # Only mount the filepath if it exists.
        logger.log_data('Mount', iso_image_filepath)
        command = 'mount --options loop "%s" "%s"' % (
            iso_image_filepath,
            iso_image_mount_point)
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Unable to mount', result)


def delete_iso_mount(iso_image_mount_point, thread):
    logger.log_note('Delete ISO image mount point %s' % iso_image_mount_point)

    iso_image_mount_point = os.path.realpath(iso_image_mount_point)

    if os.path.exists(iso_image_mount_point):

        # Unmount existing mount point, just in case it is already
        # mounted.

        logger.log_data('Unmount if it is mounted', iso_image_mount_point)
        command = 'umount "%s"' % iso_image_mount_point
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Unable to unmount', result)
        time.sleep(1.00)

        # Delete the mount point.
        logger.log_data('Delete mount point', iso_image_mount_point)
        command = 'rm -rf "%s"' % iso_image_mount_point
        result, error = execute_synchronous(command, thread)
        if error:
            logger.log_data('Unable to delete', result)
        time.sleep(1.00)

    else:

        logger.log_data('The mount point does not exist', 'Do nothing')


########################################################################
# Get Iso Image Information
########################################################################


def get_iso_image_volume_id(iso_image_filepath, thread):
    # logger.log_data('Get ISO image volume id')
    # Get the original ISO image volume id.
    iso_image_filepath = os.path.realpath(iso_image_filepath)
    command = 'isoinfo -d -i "%s"' % iso_image_filepath
    result, error = execute_synchronous(command, thread)
    iso_image_volume_id = 'Unknown iso image volume id'
    if not error:
        iso_image_volume_id = re.sub(
            r'.*Volume id:\s+(.*[^\n]).*Volume\s+set\s+id.*',
            r'\1',
            result,
            0,
            re.DOTALL)
    return iso_image_volume_id


def get_iso_image_release_name(iso_image_mount_point, thread):
    # logger.log_data('Get ISO image release name')
    iso_image_mount_point = os.path.realpath(iso_image_mount_point)
    # Read the original ISO image README.diskdefines file.
    command = 'cat "%s"' % os.path.join(
        iso_image_mount_point,
        'README.diskdefines')
    result, error = execute_synchronous(command, thread)
    # Get the original ISO image release name.
    iso_image_release_name = 'Unknown iso image release name'
    if not error:
        iso_image_release_name_infromation = re.search(
            r'DISKNAME.*"(.*)"',
            result)
        if iso_image_release_name_infromation:
            iso_image_release_name = iso_image_release_name_infromation.group(
                1)
    return iso_image_release_name


def get_iso_image_disk_name(iso_image_mount_point, thread):
    # logger.log_data('Get ISO image disk name')
    iso_image_mount_point = os.path.realpath(iso_image_mount_point)
    # Read the original ISO image README.diskdefines file.
    command = 'cat "%s"' % os.path.join(
        iso_image_mount_point,
        'README.diskdefines')
    result, error = execute_synchronous(command, thread)
    # Get the original ISO image disk name.
    iso_image_disk_name = 'Unknown iso image disk name'
    if not error:
        iso_image_disk_name_information = re.search(r'DISKNAME *(.*)', result)
        if iso_image_disk_name_information:
            iso_image_disk_name = iso_image_disk_name_information.group(1)
    return iso_image_disk_name


def get_casper_relative_directory(iso_image_mount_point):
    # logger.log_data('Get casper relative directory')
    casper_directory = get_directory_for_file(
        'filesystem.squashfs',
        iso_image_mount_point)
    casper_relative_directory = os.path.relpath(
        casper_directory,
        iso_image_mount_point)
    return casper_relative_directory


########################################################################
# Creators
########################################################################


def create_custom_iso_image_version_number():
    # logger.log_data('Create custom ISO version number')
    return datetime.datetime.now().strftime('%Y.%m.%d')


def create_configuration_filepath(project_directory):
    # logger.log_data('Create configuration filepath')
    return os.path.join(project_directory, 'cubic.conf')


def create_original_iso_image_mount_point(project_directory):
    # logger.log_data('Create original ISO image mount point')
    return os.path.join(project_directory, 'original-iso-mount')


def create_custom_squashfs_directory(project_directory):
    # logger.log_data('Create custom squashfs directory')
    return os.path.join(project_directory, 'squashfs-root')


def create_custom_live_iso_directory(project_directory):
    # logger.log_data('Create custom live ISO directory')
    return os.path.join(project_directory, 'custom-live-iso')


def create_custom_iso_image_filename(
        original_iso_image_filename,
        custom_iso_image_version_number):
    logger.log_note('Create custom ISO image filename')
    logger.log_data(
        'The original ISO image filename is',
        original_iso_image_filename)
    logger.log_data(
        'The custom ISO image version number is',
        custom_iso_image_version_number)

    if original_iso_image_filename:

        # original_iso_image_filename = re.sub('\.iso$', '',
        #                                      original_iso_image_filename)
        original_iso_image_filename = original_iso_image_filename[:-4]

        # original_iso_image_filename ◀ (text_a)(version)(text_b)
        search = r'(^.*)(\d{4}\.\d{2}\.\d{2})(.*$)'
        match = re.search(search, original_iso_image_filename)
        if match:
            # Version exists in original_iso_image_filename.
            text_a = match.group(1)
            version = match.group(2)
            text_b = match.group(3)
            logger.log_data('• text a', text_a)
            logger.log_data('• version', version)
            logger.log_data('• text b', text_b)
            # text_a ◀ (text_c)(release)(point_release)(text_d)
            search = r'(^.*?)(\d{2}\.\d{1,2})(\.\d{1,2}){0,1}(.*$)'
            match = re.search(search, text_a)
            if match:
                # Release exists in text_a.
                text_c = match.group(1)
                release = match.group(2)
                point_release = match.group(3)
                text_d = match.group(4)
                logger.log_data('• text c', text_c)
                logger.log_data('• release', release)
                logger.log_data('• point release', point_release)
                logger.log_data('• text d', text_d)
                if not point_release:
                    point_release = '.0'
                    logger.log_data('• new point_release', point_release)
                    # text_a = text_c + release + point_release + text_d
                    text_a = '%s%s%s%s' % (
                        text_c,
                        release,
                        point_release,
                        text_d)
                    logger.log_data('• new text a', text_a)
            else:
                # text_b ◀ (text_c)(release)(point_release)(text_d)
                match = re.search(search, text_b)
                if match:
                    # Release exists in text_b.
                    text_c = match.group(1)
                    release = match.group(2)
                    point_release = match.group(3)
                    text_d = match.group(4)
                    logger.log_data('• text c', text_c)
                    logger.log_data('• release', release)
                    logger.log_data('• point release', point_release)
                    logger.log_data('• text d', text_d)
                    if not point_release:
                        point_release = '.0'
                        logger.log_data('• new point_release', point_release)
                        # text_b = text_c + release + point_release + text_d
                        text_b = '%s%s%s%s' % (
                            text_c,
                            release,
                            point_release,
                            text_d)
                        logger.log_data('• new text b', text_b)
            # custom_iso_image_filename = text_a + custom_iso_image_version_number + text_b + '.iso'
            custom_iso_image_filename = '%s%s%s.iso' % (
                text_a,
                custom_iso_image_version_number,
                text_b)
        else:
            # original_volume_id ◀ (text_a)(release)(point_release)(text_b)
            search = r'(^.*?)(\d{2}\.\d{1,2})(\.\d{1,2}){0,1}(.*$)'
            match = re.search(search, original_iso_image_filename)
            if match:
                # Release exists in original_iso_image_filename.
                text_a = match.group(1)
                release = match.group(2)
                point_release = match.group(3)
                text_b = match.group(4)
                logger.log_data('• text a', text_a)
                logger.log_data('• release', release)
                logger.log_data('• point release', point_release)
                logger.log_data('• text b', text_b)
                if not point_release:
                    point_release = '.0'
                    logger.log_data('• new point_release', point_release)
                # custom_iso_image_filename = text_a + release + point_release + '-' + custom_iso_image_version_number + text_b + '.iso'
                custom_iso_image_filename = '%s%s%s-%s%s.iso' % (
                    text_a,
                    release,
                    point_release,
                    custom_iso_image_version_number,
                    text_b)
            else:
                # custom_iso_image_filename = original_iso_image_filename + '-' + custom_iso_image_version_number + '.iso'
                custom_iso_image_filename = '%s-%s.iso' % (
                    original_iso_image_filename,
                    custom_iso_image_version_number)

        logger.log_data(
            'The custom iso image filename is',
            custom_iso_image_filename)

    else:

        custom_iso_image_filename = None
        logger.log_data(
            'The custom iso image filename is',
            custom_iso_image_filename)

    return custom_iso_image_filename


def create_custom_iso_image_volume_id(
        original_iso_image_volume_id,
        custom_iso_image_version_number):
    logger.log_note('Create custom ISO image volume id')
    logger.log_data(
        'The original ISO image volume id is',
        original_iso_image_volume_id)
    logger.log_data(
        'The custom ISO image version number is',
        custom_iso_image_version_number)

    if original_iso_image_volume_id:

        # original_iso_image_volume_id ◀ (text_a)(version)(text_b)
        search = r'(^.*)(\d{4}\.\d{2}\.\d{2})(.*$)'
        match = re.search(search, original_iso_image_volume_id)
        if match:
            # Version exists in original_iso_image_volume_id.
            text_a = match.group(1)
            version = match.group(2)
            text_b = match.group(3)
            logger.log_data('• text a', text_a)
            logger.log_data('• version', version)
            logger.log_data('• text b', text_b)
            # text_a ◀ (text_c)(release)(point_release)(text_d)
            search = r'(^.*?)(\d{2}\.\d{1,2})(\.\d{1,2}){0,1}(.*$)'
            match = re.search(search, text_a)
            if match:
                # Release exists in text_a.
                text_c = match.group(1)
                release = match.group(2)
                point_release = match.group(3)
                text_d = match.group(4)
                logger.log_data('• text c', text_c)
                logger.log_data('• release', release)
                logger.log_data('• point release', point_release)
                logger.log_data('• text d', text_d)
                if not point_release:
                    point_release = '.0'
                    logger.log_data('• new point_release', point_release)
                    # text_a = text_c + release + point_release + text_d
                    text_a = '%s%s%s%s' % (
                        text_c,
                        release,
                        point_release,
                        text_d)
                    logger.log_data('• new text a', text_a)
            else:
                # text_b ◀ (text_c)(release)(point_release)(text_d)
                match = re.search(search, text_b)
                if match:
                    # Release exists in text_b.
                    text_c = match.group(1)
                    release = match.group(2)
                    point_release = match.group(3)
                    text_d = match.group(4)
                    logger.log_data('• text c', text_c)
                    logger.log_data('• release', release)
                    logger.log_data('• point release', point_release)
                    logger.log_data('• text d', text_d)
                    if not point_release:
                        point_release = '.0'
                        logger.log_data('• new point_release', point_release)
                        # text_b = text_c + release + point_release + text_d
                        text_b = '%s%s%s%s' % (
                            text_c,
                            release,
                            point_release,
                            text_d)
                        logger.log_data('• new text b', text_b)
            # custom_iso_image_volume_id = text_a + custom_iso_image_version_number + text_b
            custom_iso_image_volume_id = '%s%s%s' % (
                text_a,
                custom_iso_image_version_number,
                text_b)
        else:
            # original_volume_id ◀ (text_a)(release)(point_release)(text_b)
            search = r'(^.*?)(\d{2}\.\d{1,2})(\.\d{1,2}){0,1}(.*$)'
            match = re.search(search, original_iso_image_volume_id)
            if match:
                # Release exists in original_iso_image_volume_id.
                text_a = match.group(1)
                release = match.group(2)
                point_release = match.group(3)
                text_b = match.group(4)
                logger.log_data('• text a', text_a)
                logger.log_data('• release', release)
                logger.log_data('• point release', point_release)
                logger.log_data('• text b', text_b)
                if not point_release:
                    point_release = '.0'
                    logger.log_data('• new point_release', point_release)
                # custom_iso_image_volume_id = text_a + release + point_release + ' ' + custom_iso_image_version_number + text_b
                custom_iso_image_volume_id = '%s%s%s %s%s' % (
                    text_a,
                    release,
                    point_release,
                    custom_iso_image_version_number,
                    text_b)
            else:
                # custom_iso_image_volume_id = original_iso_image_volume_id + ' ' + custom_iso_image_version_number
                custom_iso_image_volume_id = '%s %s' % (
                    original_iso_image_volume_id,
                    custom_iso_image_version_number)

        logger.log_data(
            'The custom iso image volume id is',
            custom_iso_image_volume_id)

    else:

        custom_iso_image_volume_id = None
        logger.log_data(
            'The custom iso image volume id is',
            custom_iso_image_volume_id)

    return custom_iso_image_volume_id


def create_custom_iso_image_release_name(original_iso_image_release_name):
    # logger.log_data('Create custom ISO image release name')

    try:
        custom_iso_image_release_name = 'Custom %s' % re.sub(
            r'^Custom\s*',
            '',
            original_iso_image_release_name)
    except Exception as exception:
        logger.log_data(
            'Encountered exception while creating custom ISO image release name',
            exception)
        custom_iso_image_release_name = ''

    # logger.log_data('The created custom ISO image release name is', custom_iso_image_release_name)
    return custom_iso_image_release_name


def create_custom_iso_image_disk_name(
        custom_iso_image_volume_id,
        custom_iso_image_release_name):
    # logger.log_note('Create custom ISO image disk name')

    if custom_iso_image_volume_id and custom_iso_image_release_name:
        custom_iso_image_disk_name = '%s "%s"' % (
            custom_iso_image_volume_id,
            custom_iso_image_release_name)
    elif custom_iso_image_volume_id:
        custom_iso_image_disk_name = custom_iso_image_volume_id
    elif custom_iso_image_release_name:
        custom_iso_image_disk_name = custom_iso_image_release_name
    else:
        custom_iso_image_disk_name = ''

    # logger.log_data('The created custom ISO image disk name is', custom_iso_image_disk_name)
    return custom_iso_image_disk_name


def create_custom_iso_image_md5_filename_ORIGINAL(custom_iso_image_filename):
    # logger.log_data('Create custom ISO image md5 filename')

    try:
        custom_iso_image_md5_filename = re.sub(
            r'\.iso$|\.$|$',
            '.md5',
            custom_iso_image_filename)
    except Exception as exception:
        logger.log_data(
            'Encountered exception while creating custom ISO image md5 filename',
            exception)
        custom_iso_image_md5_filename = 'custom.md5'

    # logger.log_data('The created custom ISO image md5 filename is', custom_iso_image_md5_filename)
    return custom_iso_image_md5_filename


def create_custom_iso_image_md5_filename(custom_iso_image_filename):
    # logger.log_data('Create custom ISO image md5 filename')
    try:
        # filename_root = os.path.splitext(custom_iso_image_filename)[0]
        # filename_root = re.search(r'(.*?)\.iso*', custom_iso_image_filename).group(1)
        # filename_root = re.search(r'(.*?)(?:(?:\.iso)*)$', custom_iso_image_filename).group(1)
        custom_iso_image_md5_filename = '%s.md5' % custom_iso_image_filename[:
                                                                             -4]
    except Exception as exception:
        logger.log_data(
            'Encountered exception while creating custom ISO image md5 filename',
            exception)
        custom_iso_image_md5_filename = 'custom.md5'
    # logger.log_data('The created custom ISO image md5 filename is', custom_iso_image_md5_filename)
    return custom_iso_image_md5_filename


########################################################################
# Copy Files Functions
########################################################################


def create_file_details_list():
    # logger.log_data('List files to copy')

    file_details_list = []

    for file_number, uri in enumerate(model.uris):
        filepath = unquote(urlparse(uri).path)
        file_details_list.append([0, filepath])

    return file_details_list


def copy_files(thread):
    logger.log_note('Copy file(s)')

    total_files = len(model.uris)
    current_directory = get_current_directory()
    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    relative_directory = os.path.join(
        '/',
        os.path.relpath(current_directory,
                        custom_squashfs_directory))

    logger.log_data('The current directory is', current_directory)
    logger.log_data(
        'The custom squashfs directory is',
        model.custom_squashfs_directory)
    logger.log_data(
        'The real custom squashfs directory is',
        custom_squashfs_directory)
    logger.log_data('The relative current directory is', relative_directory)

    for file_number, uri in enumerate(model.uris):

        filepath = unquote(urlparse(uri).path)

        if total_files == 1:
            label = 'Copying one file to %s' % relative_directory
        else:
            label = 'Copying file %s of %s to %s' % (
                file_number + 1,
                total_files,
                relative_directory)

        display.update_label('copy_files_page__progress_label', label)
        display.scroll_to_tree_view_row(
            'copy_files_page__treeview',
            file_number)

        copy_file(
            filepath,
            file_number,
            current_directory,
            total_files,
            thread)

        time.sleep(0.10)


def copy_file(filepath, file_number, directory, total_files, thread):
    logger.log_data(
        'Copy file',
        'Number %s of %s' % (file_number + 1,
                             total_files))
    logger.log_data('The file is', filepath)
    logger.log_data('The target directory is', directory)

    command = 'rsync --archive --info=progress2 "%s" "%s"' % (
        filepath,
        directory)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread)
    logger.log_data('• The start time is', formatted_time)

    progress_initial_global = int(round(100 * file_number / total_files, 0))

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    pulse = max(0.01 / total_files, .001)
    pause = max(1 / total_files, .01)

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):

        try:
            line = thread.process.read_nonblocking(100, 0.05)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(pulse)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'copy_files_page__copy_files_progressbar',
                    None)
                display.update_liststore_progressbar_percent(
                    'copy_files_page__file_details__liststore',
                    file_number,
                    0)
            display.update_progressbar_percent(
                'copy_files_page__copy_files_progressbar',
                progress_initial_global + progress_display / total_files)
            display.update_liststore_progressbar_percent(
                'copy_files_page__file_details__liststore',
                file_number,
                progress_display)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    time.sleep(pause)


########################################################################
# Enter Chroot Environment Functions
########################################################################


def copy_original_iso_files(thread):
    logger.log_note('Copy the original ISO files')

    # Note: source_path and target_path must end in "/"

    original_iso_image_mount_point = os.path.realpath(
        model.original_iso_image_mount_point)
    source_path = os.path.join(original_iso_image_mount_point, '')
    logger.log_data('The source path is', source_path)

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    target_path = os.path.join(custom_live_iso_directory, '')
    logger.log_data('The target path is', target_path)

    # filepath = os.path.join(custom_live_iso_directory, model.casper_relative_directory, 'filesystem.manifest-remove')
    # is_exists = os.path.exists(filepath)

    filename = 'filesystem.manifest-remove'
    is_exists_filesystem_manifest_typical_remove = is_exists_filesystem_manifest_remove(
        filename)
    logger.log_data(
        'Include %s?' % filename,
        not is_exists_filesystem_manifest_typical_remove)

    filename = 'filesystem.manifest-minimal-remove'
    is_exists_filesystem_manifest_minimal_remove = is_exists_filesystem_manifest_remove(
        filename)
    logger.log_data(
        'Include %s?' % filename,
        not is_exists_filesystem_manifest_minimal_remove)

    if not is_exists_filesystem_manifest_typical_remove and not is_exists_filesystem_manifest_minimal_remove:
        # Copy all files from the original iso.
        # Exclude or copy the following files as indicated.
        # Do not copy: /md5sum.txt
        # Do not copy: /casper/filesystem.manifest
        # ****** Copy: /casper/filesystem.manifest-remove
        # ****** Copy: /casper/filesystem.manifest-minimal-remove
        # Do not copy: /casper/filesystem.size
        # Do not copy: /casper/filesystem.squashfs
        # Do not copy: /casper/filesystem.squashfs.gpg
        # Do not copy: /casper/initrd.lz
        # Do not copy: /casper/vmlinuz.efi

        command = (
            'rsync'
            ' --delete'
            ' --archive'
            ' --exclude="md5sum.txt"'
            ' --exclude="/%s/filesystem.squashfs"'
            ' --exclude="/%s/filesystem.squashfs.gpg"'
            ' --progress "%s" "%s"' % (
                model.casper_relative_directory,
                model.casper_relative_directory,
                source_path,
                target_path))
    elif is_exists_filesystem_manifest_typical_remove and not is_exists_filesystem_manifest_minimal_remove:
        # Copy all files from the original iso.
        # Exclude or copy the following files as indicated.
        # Do not copy: /md5sum.txt
        # Do not copy: /casper/filesystem.manifest
        # Do not Copy: /casper/filesystem.manifest-remove
        # ****** Copy: /casper/filesystem.manifest-minimal-remove
        # Do not copy: /casper/filesystem.size
        # Do not copy: /casper/filesystem.squashfs
        # Do not copy: /casper/filesystem.squashfs.gpg
        # Do not copy: /casper/initrd.lz
        # Do not copy: /casper/vmlinuz.efi

        command = (
            'rsync'
            ' --delete'
            ' --archive'
            ' --exclude="md5sum.txt"'
            ' --exclude="/%s/filesystem.squashfs"'
            ' --exclude="/%s/filesystem.squashfs.gpg"'
            ' --exclude="/%s/filesystem.manifest-remove"'
            # ' --exclude="/%s/filesystem.manifest-minimal-remove"'
            ' --progress "%s" "%s"' % (
                model.casper_relative_directory,
                model.casper_relative_directory,
                model.casper_relative_directory,
                source_path,
                target_path))
    elif not is_exists_filesystem_manifest_typical_remove and is_exists_filesystem_manifest_minimal_remove:
        # Copy all files from the original iso.
        # Exclude or copy the following files as indicated.
        # Do not copy: /md5sum.txt
        # Do not copy: /casper/filesystem.manifest
        # ****** Copy: /casper/filesystem.manifest-remove
        # Do not Copy: /casper/filesystem.manifest-minimal-remove
        # Do not copy: /casper/filesystem.size
        # Do not copy: /casper/filesystem.squashfs
        # Do not copy: /casper/filesystem.squashfs.gpg
        # Do not copy: /casper/initrd.lz
        # Do not copy: /casper/vmlinuz.efi

        command = (
            'rsync'
            ' --delete'
            ' --archive'
            ' --exclude="md5sum.txt"'
            ' --exclude="/%s/filesystem.squashfs"'
            ' --exclude="/%s/filesystem.squashfs.gpg"'
            # ' --exclude="/%s/filesystem.manifest-remove"'
            ' --exclude="/%s/filesystem.manifest-minimal-remove"'
            ' --progress "%s" "%s"' % (
                model.casper_relative_directory,
                model.casper_relative_directory,
                source_path,
                target_path))
    else:
        # Copy all files from the original iso.
        # Exclude or copy the following files as indicated.
        # Do not copy: /md5sum.txt
        # Do not copy: /casper/filesystem.manifest
        # Do not copy: /casper/filesystem.manifest-remove
        # Do not Copy: /casper/filesystem.manifest-minimal-remove
        # Do not copy: /casper/filesystem.size
        # Do not copy: /casper/filesystem.squashfs
        # Do not copy: /casper/filesystem.squashfs.gpg
        # Do not copy: /casper/initrd.lz
        # Do not copy: /casper/vmlinuz.efi

        command = (
            'rsync'
            ' --delete'
            ' --archive'
            ' --exclude="md5sum.txt"'
            ' --exclude="/%s/filesystem.squashfs"'
            ' --exclude="/%s/filesystem.squashfs.gpg"'
            ' --progress "%s" "%s"' % (
                model.casper_relative_directory,
                model.casper_relative_directory,
                source_path,
                target_path))

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread)
    logger.log_data('• The start time is', formatted_time)

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):

        try:
            line = thread.process.read_nonblocking(100, 0.05)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(0.05)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'unsquashfs_page__copy_original_iso_files_progressbar',
                    None)
            display.update_progressbar_percent(
                'unsquashfs_page__copy_original_iso_files_progressbar',
                progress_display)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    time.sleep(0.10)

    # TODO: Set return value based on rsync result.
    return True


def extract_squashfs(thread):
    logger.log_note('Extract squashfs')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    target_path = custom_squashfs_directory
    logger.log_data('The target path is', target_path)

    # Delete custom squashfs directory, if it exists.
    delete_file(target_path, thread)

    original_iso_image_mount_point = os.path.realpath(
        model.original_iso_image_mount_point)
    source_path = os.path.join(
        original_iso_image_mount_point,
        model.casper_relative_directory,
        'filesystem.squashfs')
    logger.log_data('The source path is', source_path)

    command = 'unsquashfs -force -dest "%s" "%s"' % (target_path, source_path)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread)
    logger.log_data('• The start time is', formatted_time)

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):
        try:
            line = thread.process.read_nonblocking(100, 0.05)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(0.05)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'unsquashfs_page__unsquashfs_progressbar',
                    None)
            display.update_progressbar_percent(
                'unsquashfs_page__unsquashfs_progressbar',
                progress_display)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    time.sleep(0.10)

    # TODO: Set return value based on rsync result.
    return True


def prepare_chroot_environment(thread):

    _prepare_chroot_environment(thread)


def _prepare_chroot_environment_TESTING(thread):

    logger.log_note('Prepare chroot environment (Testing)')


# Vte Terminal Information
# https://lazka.github.io/pgi-docs/#Vte-2.91/classes/Terminal.html
# https://help.ubuntu.com/community/BasicChroot
def _prepare_chroot_environment(thread):
    logger.log_note('Prepare chroot environment')

    # Removed xhost for bug #1766374
    # # command = 'xhost +local:'
    # command = 'xhost +'
    # execute_synchronous(command, thread)

    # command = 'export DISPLAY=:0.0'
    # result, error = execute_synchronous(command, thread)
    # if (error == 0):
    #     logger.log_note('Successfully exported the display')
    # else:
    #     logger.log_note('There was an error exporting the display')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)

    command = 'mount --bind /dev "%s"' % os.path.join(
        custom_squashfs_directory,
        'dev')
    result, error = execute_synchronous(command, thread)
    if error: logger.log_data('Error mounting /dev', result)

    command = 'mount --bind /run "%s"' % os.path.join(
        custom_squashfs_directory,
        'run')
    result, error = execute_synchronous(command, thread)
    if error: logger.log_data('Error mounting /run', result)

    #
    # Added to fix Bug #177857, 'out of pty devices' error.
    #

    # TODO: Should we use "mount -o bind" for Ubuntu?
    #       See https://help.ubuntu.com/community/BasicChroot#Setting-up_the_chroot
    # TODO: Should we use "proc" instead of "none"?
    #       See https://unix.stackexchange.com/questions/98405/which-of-proc-sys-etc-should-be-bind-mounted-or-not-when-chrooting-into-a-r
    # command = 'mount --types proc none "%s"' % os.path.join(custom_squashfs_directory, 'proc')
    command = 'mount --types proc proc "%s"' % os.path.join(
        custom_squashfs_directory,
        'proc')
    result, error = execute_synchronous(command, thread)
    if error: logger.log_data('Error mounting /proc', result)

    # TODO: Should we use "sys" instead of "none"?
    #       See https://unix.stackexchange.com/questions/98405/which-of-proc-sys-etc-should-be-bind-mounted-or-not-when-chrooting-into-a-r
    # command = 'mount --types sysfs none "%s"' % os.path.join(custom_squashfs_directory, 'sys')
    command = 'mount --types sysfs sys "%s"' % os.path.join(
        custom_squashfs_directory,
        'sys')
    result, error = execute_synchronous(command, thread)
    if error: logger.log_data('Error mounting /sys', result)

    # TODO: Should we use "pts" instead of "none"?
    #       See https://unix.stackexchange.com/questions/98405/which-of-proc-sys-etc-should-be-bind-mounted-or-not-when-chrooting-into-a-r
    # command = 'mount --types devpts none "%s"' % os.path.join(custom_squashfs_directory, 'dev', 'pts')
    command = 'mount --types devpts pts "%s"' % os.path.join(
        custom_squashfs_directory,
        'dev',
        'pts')
    result, error = execute_synchronous(command, thread)
    if error: logger.log_data('Error mounting /dev/pts', result)

    # Attempt to fix dbus issues such as:
    #   Rendering 'assets/selectionmode-checkbox-unchecked.png'
    #   No protocol specified
    #   Failed to get connection
    #   ** (inkscape:25672): CRITICAL **: 17:58:24.770: dbus_g_proxy_new_for_name: assertion 'connection != NULL' failed
    #
    # command = 'mount --bind /run/dbus "%s"' % os.path.join(
    #     custom_squashfs_directory,
    #     'run',
    #     'dbus')
    # result, error = execute_synchronous(command, thread)
    # if error: logger.log_data('Error mounting /run/dbus', result)

    # See if machine-id needs to be set on live ISOs?
    # We may be able to get away with not setting this, since
    # 1. /var/lib/dbus is not always present.
    # 2. /etc/machine-id is used on some systems.
    #
    # Consider using system-machine-id-setup, if command is available.
    # This will generate /etc/machine-id, so create a symlink from
    # /var/lib/dbus/machine-id to /etc/machine-id
    '''
    filepath = os.path.join(
        custom_squashfs_directory,
        'var',
        'lib',
        'dbus',
        'machine-id')
    if os.path.exists(filepath):
        machine_id = str(uuid.uuid4()).replace('-', '')
        with open(filepath, 'w') as file:
            file.write('%s' % machine_id)
        logger.log_data('The new machine id is', machine_id)
    else:
        logger.log_data('Not setting machine id because file does not exist', filepath)
    '''

    # Update .bashrc. This file will be restored in function
    # initialize_chroot_environmrnt().
    try:
        logger.log_note('Change terminal prompt colors (modify .bashrc)')
        # Make a backup of .bashrc
        source_filepath = os.path.join(
            custom_squashfs_directory,
            'root',
            '.bashrc')
        target_filepath = os.path.join(
            custom_squashfs_directory,
            'root',
            '.bashrc.bak')
        logger.log_data('Backup', source_filepath)
        logger.log_data('To', target_filepath)
        copyfile(source_filepath, target_filepath)
        # Change terminal prompt colors.
        filepath = os.path.join(custom_squashfs_directory, 'root', '.bashrc')
        replace_text_in_file(
            filepath,
            '#force_color_prompt=yes',
            'force_color_prompt=yes')
        replace_text_in_file(filepath, '01;32', '00;35')
        replace_text_in_file(filepath, '01;34', '00;36')
        replace_text_in_file(filepath, r']\\\$', r'] \$')
    # except IOError as exception:
    except Exception as exception:
        logger.log_data(
            'Ignoring exception while changing terminal prompt colors (modifying .bashrc)',
            exception)


def enter_chroot_environment(*args):

    _enter_chroot_environment(args)


# This function is used for testing only. It "randomly" decides to enter
# the chroot environment.
def _enter_chroot_environment_TESTING(*args):
    # thread = args[0]
    should_enter_chroot = bool(int(time.strftime('%s')) % 2)
    if should_enter_chroot:
        # If the current time seconds is an odd number, enter chroot.
        print()
        print(BOLD_YELLOW + 'Enter chroot environment (Testing).' + NORMAL)
        print()
        custom_squashfs_directory = os.path.realpath(
            model.custom_squashfs_directory)
        os.chroot(custom_squashfs_directory)
    else:
        # If the current time seconds is an even number, do not enter chroot.
        print()
        print(
            BOLD_RED + 'Error entering chroot environment (Testing)' + NORMAL)
        print()


def _enter_chroot_environment(*args):
    try:
        # thread = args[0]
        print()
        print(BOLD_YELLOW + 'Enter chroot environment.' + NORMAL)
        print()
        custom_squashfs_directory = os.path.realpath(
            model.custom_squashfs_directory)
        os.chroot(custom_squashfs_directory)
    except Exception as exception:
        print()
        print(BOLD_RED + 'Error entering chroot environment' + NORMAL)
        print()


# Vte Terminal Information
# https://lazka.github.io/pgi-docs/#Vte-2.91/classes/Terminal.html
# https://web.archive.org/web/20170311221231/https://lazka.github.io/pgi-docs/Vte-2.91/classes/Terminal.html#Vte.Terminal.feed_child
def create_chroot_terminal(thread):
    logger.log_note('Enter chroot environment')
    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    logger.log_data(
        'The chroot environment directory is',
        custom_squashfs_directory)

    terminal = model.builder.get_object('terminal_page__terminal')
    terminal.reset(True, False)
    settings = Gio.Settings('org.gnome.desktop.interface')
    font_name = settings.get_string('monospace-font-name')
    font = Pango.FontDescription(font_name)
    terminal.set_font(font)
    # terminal.set_scrollback_lines(-1)

    flags = Gtk.DestDefaults.MOTION | Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP
    # TODO: Change: Gtk.TargetFlags
    #       See: https://lazka.github.io/pgi-docs/Gtk-3.0/structs/TargetEntry.html#methods
    targets = [
        Gtk.TargetEntry.new('text/uri-list',
                            0,
                            80),
        Gtk.TargetEntry.new('text/plain',
                            0,
                            80)
    ]
    actions = Gdk.DragAction.COPY
    terminal.drag_dest_set(flags, targets, actions)

    pty_flags = PtyFlags.DEFAULT
    working_directory = os.path.join(custom_squashfs_directory, 'root')
    terminal_argument_vector = ['/bin/bash', '--login']
    environment_variables = [
        'HOME=/root',
        'DISPLAY=%s' % (os.environ['DISPLAY'])
    ]
    # spawn_flags = GLib.SpawnFlags.DO_NOT_REAP_CHILD
    spawn_flags = GLib.SpawnFlags.DEFAULT
    terminal_setup_data = thread

    # https://lazka.github.io/pgi-docs/#Vte-2.90/classes/Terminal.html
    # https://lazka.github.io/pgi-docs/#Vte-2.91/classes/Terminal.html
    # https://developer.gnome.org/vte/unstable/VteTerminal.html#vte-terminal-spawn-async

    # TODO: spawn_sync is deprecated, use spawn_async

    try:

        terminal.spawn_sync

    except AttributeError:

        # Ubuntu 14.04 uses libvte-2.90
        # For Vte 2.90 use fork_command_full()...
        # terminal_pid = int(terminal.fork_command_full(pty_flags, logger.log_data('Creating a terminal widget using function', 'fork_command_full(); libvte-2.90+; Ubuntu 14.04+')
        terminal_pid = int(
            terminal.fork_command_full(
                pty_flags,
                working_directory,
                terminal_argument_vector,
                environment_variables,
                spawn_flags,
                enter_chroot_environment,
                terminal_setup_data)[1])
        model.set_terminal_pid(terminal_pid)

        # # Clear the terminal.
        # # Work-around for Bug #1550003
        # # In Ubuntu 14.04, the first few lines of text in in the Terminal are not visible.
        # # See https://bugs.launchpad.net/cubic/+bug/1779015
        # text = 'clear'
        # send_command_to_terminal(text)

    else:

        # Ubuntu 15.04 uses libvte-2.91
        # For Vte 2.91 use spawn_sync()...
        # terminal_pid = int(terminal.spawn_sync(pty_flags, logger.log_data('Creating a terminal widget using function', 'spawn_sync(); libvte-2.91+; Ubuntu 15.04+')
        terminal_pid = int(
            terminal.spawn_sync(
                pty_flags,
                working_directory,
                terminal_argument_vector,
                environment_variables,
                spawn_flags,
                enter_chroot_environment,
                terminal_setup_data)[1])
        model.set_terminal_pid(terminal_pid)

        # # Clear the terminal.
        # # Work-around for Bug in Ubuntu 15.04+, where the bottom of the terminal appears shaded.
        # # See https://bugs.launchpad.net/cubic/+bug/1779015
        # text = 'clear'
        # send_command_to_terminal(text)

    # Enable input to the terminal.
    # terminal.set_input_enabled(True)
    display.set_sensitive('terminal_page__terminal', True)


def check_chroot(thread):
    logger.log_note('Check chroot environment')

    logger.log_data('The terminal pid is', model.terminal_pid)

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    logger.log_data(
        'The custom squashfs directory is',
        custom_squashfs_directory)

    terminal_root_directory = None
    try:
        terminal_root_directory = os.readlink(
            '/proc/%s/root' % model.terminal_pid)
    except FileNotFoundError as exception:
        pass
    logger.log_data(
        'The termnal\'s root directory is',
        terminal_root_directory)

    is_chroot = (terminal_root_directory == custom_squashfs_directory)

    logger.log_data('Terminal is in chroot environment?', is_chroot)
    return is_chroot


def initialize_chroot_environment(thread):
    logger.log_note('Initialize chroot environment')

    is_chroot = check_chroot(thread)

    # Note:
    #
    # The message "mesg: ttyname failed: No such device" apears just before
    # the status is printed to the chroot terminal. This is probably bug in
    # the .profile file.
    #
    # The cause of the problem is that the line "mesg n || true" in .profile
    # runs every time bash is executed, even when it is run from a session
    # without a tty device.
    #
    # Solution 1:
    # In file... ".profile"
    # Replace... mesg n || true
    # With...... if [[ $( tty ) != "not a tty" ]]; then mesg n || true; fi

    # Solution 1 Command:
    # $ sed -i 's/^mesg n || true$/if [[ $( tty ) != \"not a tty\" ]]; then mesg n || true; fi/g' .profile
    #
    # Solution 2:
    # In file... ".profile"
    # Replace... mesg n || true
    # With...... (tty > /dev/null) && (mesg n || true)
    #
    # Solution 2 Command:
    # $ sed -i 's/^mesg n || true$/(tty > /dev/null) && (mesg n || true)/g' .profile
    #
    # Reference:
    # https://bugs.launchpad.net/cubic/+bug/1779675/comments/4
    # https://superuser.com/questions/1241548/xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device

    if is_chroot:

        # Notify user that we are in chroot.
        text = BOLD_GREEN + 'You are in the chroot environment.' + NORMAL
        send_message_to_terminal(text)

        # Divert initctl.
        text = 'dpkg-divert --local --rename --add /sbin/initctl'
        send_command_to_terminal(text)

        # Enter a new line.
        text = ''
        send_command_to_terminal(text)

    else:

        # Notify user that we are not in chroot.
        text = BOLD_RED + 'WARNING! You are in NOT the chroot environment. Exiting.' + NORMAL
        send_message_to_terminal(text)

        # If not in chroot, exit the terminal. Once the terminal exits,
        # the function handlers.on_child_exited__terminal_page() will be
        # invoked.
        text = 'exit'
        send_command_to_terminal(text)

        # Enter a new line.
        send_command_to_terminal()

    # Restore .bashrc. This file was changed in function
    # prepare_chroot_environment(thread)
    try:
        logger.log_note('Restore terminal prompt colors (restore .bashrc)')
        custom_squashfs_directory = os.path.realpath(
            model.custom_squashfs_directory)
        source_filepath = os.path.join(
            custom_squashfs_directory,
            'root',
            '.bashrc.bak')
        target_filepath = os.path.join(
            custom_squashfs_directory,
            'root',
            '.bashrc')
        logger.log_data('Restore', target_filepath)
        logger.log_data('From', source_filepath)
        move(source_filepath, target_filepath)
    # except IOError as exception:
    except Exception as exception:
        logger.log_data(
            'Ignoring exception while restoring terminal prompt colors (restoring .bashrc)',
            exception)


# Terminal.feed() may require one or two arguments:
# - feed(text, length)
# - feed(bytes)
# After executing Terminal.feed(), it is necessary to execute
# Terminal.feed_child() to print a new line.
#
# However, Terminal.feed_child() may also require one or two arguments:
# - feed_child(text, length)
# - feed_child(bytes)
#
# The approach used here allows any combination of Terminal.feed(), with one or
# two arguments, and Terminal.feed_child(), with one or two arguments.
def send_message_to_terminal(text=None):

    terminal = model.builder.get_object('terminal_page__terminal')

    try:
        # Using Vte.Terminal 2.90 or 2.91
        # Print the message.
        if text: terminal.feed(text + '\n', -1)
        # Print a new line. (This is necessary).
        send_command_to_terminal()
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        # Print the message.
        if text: terminal.feed(bytes(text + '\n', encoding='utf-8'))
        # Print a new line. (This is necessary).
        send_command_to_terminal()
        logger.log_data('Send bytes to terminal', text)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)


# Terminal.feed_child() may require one or two arguments:
# - feed_child(text, length)
# - feed_child(bytes)
# If text is none, a new line is sent to the terminal.
def send_command_to_terminal(text=None):

    terminal = model.builder.get_object('terminal_page__terminal')

    try:
        # Using Vte.Terminal 2.90 or 2.91
        if text: terminal.feed_child(text + '\n', -1)
        else: terminal.feed_child('\n', -1)
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        if text: terminal.feed_child(bytes(text + '\n', encoding='utf-8'))
        else: terminal.feed_child(bytes('\n', encoding='utf-8'))
        logger.log_data('Send bytes to terminal', text)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)


# Terminal.feed_child() may require one or two arguments:
# - feed_child(text, length)
# - feed_child(bytes)
# Text is sent to the terminal without appending a new line.
def send_text_to_terminal(text):

    terminal = model.builder.get_object('terminal_page__terminal')

    try:
        # Using Vte.Terminal 2.90 or 2.91
        terminal.feed_child(text, -1)
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        terminal.feed_child(bytes(text, encoding='utf-8'))
        logger.log_data('Send bytes to terminal', text)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)


########################################################################
# Exit Chroot Environment Functions
########################################################################


def get_processes_using_directory(directory):
    directory = os.path.realpath(directory)
    logger.log_data('Get processes that are using directory', directory)

    pids = []
    symlinks = glob.glob('/proc/*/root')
    for symlink in symlinks:
        try:
            target = os.readlink(symlink)
            if directory in target:
                pid = int(re.search(r'.*/(\d*)/.*', symlink).group(1))
                pids.append(pid)
        except FileNotFoundError as exception:
            pass

    if pids:
        logger.log_data(
            '%i processes were found that are using directory' % len(pids),
            directory)
        logger.log_data('%s' % pids)
        # for index, pid in enumerate(pids):
        #     logger.log_data('% 2i. %s' % (index+1, pid))
    else:
        logger.log_data(
            'No processes were found that are using directory',
            directory)

    return pids


def kill_processes(pids, exclude_pid=None):
    while pids:
        pid = pids.pop()
        if pid != exclude_pid:
            logger.log_data('Killing chroot process with pid', pid)
            os.kill(pid, signal.SIGKILL)
        else:
            logger.log_data(
                'Not killing excluded chroot process with pid',
                pid)


def get_mount_points_in_directory(directory, thread):
    # directory = os.path.realpath(directory)
    logger.log_data('Get mount points in directory', directory)

    mount_points = None
    command = 'mount'
    result, error = execute_synchronous(command, thread)
    mount_points = None
    if not error:
        mount_points = re.findall(r'.*on\s(%s.*)\stype' % directory, result)
    else:
        # logger.log_data(
        #     'Unable to get mount points in directory %s' % directory, result)
        logger.log_data('Unable to get mount points in', directory)

    if mount_points:
        logger.log_data(
            '%i mount points were found in directory' % len(mount_points),
            directory)
        for index, mount_point in enumerate(mount_points):
            logger.log_data('Mount point % 2i' % (index + 1), mount_point)
    else:
        # logger.log_data(
        #     'No mount points were found in directory %s' % directory, result)
        logger.log_data('No mount points were found in', directory)

    return mount_points


def unmount_mount_points(mount_points):
    logger.log_data('Unmount mount points')
    while mount_points:
        mount_point = mount_points.pop()
        mount_point = os.path.realpath(mount_point)
        logger.log_data('Unmount', mount_point)
        command = 'umount "%s"' % mount_point
        result, error = execute_synchronous(command)
        if not error:
            logger.log_data('Successfully unmounted %s' % mount_point, result)
        else:
            logger.log_data('Unable to unmount %s' % mount_point, result)


def exit_chroot_environment(thread):
    # http://askubuntu.com/questions/162319/how-do-i-stop-all-processes-in-a-chroot

    logger.log_note('Exit chroot environment')

    terminal = model.builder.get_object('terminal_page__terminal')

    # Disable input to the terminal.
    # terminal.set_input_enabled(False)
    display.set_sensitive('terminal_page__terminal', False)

    # Do we need this? Should this be done from outside the chroot environmant?
    # Remove file /sbin/initctl.
    # See https://bugs.launchpad.net/cubic/+bug/1779015
    text = 'rm -f /sbin/initctl'
    try:
        # Using Vte.Terminal 2.90 or 2.91
        terminal.feed_child(text, -1)
        terminal.feed_child('\n', -1)
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        data = bytes(text, encoding='utf-8')
        terminal.feed_child(data)
        terminal.feed_child(bytes('\n', encoding='utf-8'))
        logger.log_data('Send bytes to terminal', data)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)

    # Remove initctl diversion.
    # See https://bugs.launchpad.net/cubic/+bug/1779015
    text = 'dpkg-divert --rename --remove /sbin/initctl'
    try:
        # Using Vte.Terminal 2.90 or 2.91
        terminal.feed_child(text, -1)
        terminal.feed_child('\n', -1)
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        data = bytes(text, encoding='utf-8')
        terminal.feed_child(data)
        terminal.feed_child(bytes('\n', encoding='utf-8'))
        logger.log_data('Send bytes to terminal', data)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)

    # Exit the terminal.
    # See https://bugs.launchpad.net/cubic/+bug/1779015
    text = 'exit'
    try:
        # Using Vte.Terminal 2.90 or 2.91
        terminal.feed_child(text, -1)
        terminal.feed_child('\n', -1)
        logger.log_data('Send text to terminal', text)
    except TypeError:
        # Using Vte.Terminal "new" 2.91
        data = bytes(text, encoding='utf-8')
        terminal.feed_child(data)
        terminal.feed_child(bytes('\n', encoding='utf-8'))
        logger.log_data('Send bytes to terminal', data)
    # This seems necessary to avoid a race condition in Vte.Terminal.
    time.sleep(0.1)

    #
    # Attempt to remove all chroot mounts.
    #

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)

    # Attempt 1
    chroot_mount_points = get_mount_points_in_directory(
        custom_squashfs_directory,
        thread)
    if chroot_mount_points: unmount_mount_points(chroot_mount_points)

    # Attempt 2
    chroot_mount_points = get_mount_points_in_directory(
        custom_squashfs_directory,
        thread)
    if chroot_mount_points: unmount_mount_points(chroot_mount_points)

    #
    # Attempt to kill remaining processes and remove rmaining chroot
    # mounts.
    #

    # Attempt 1
    chroot_processes = get_processes_using_directory(custom_squashfs_directory)
    if chroot_processes: kill_processes(chroot_processes, model.terminal_pid)
    chroot_mount_points = get_mount_points_in_directory(
        custom_squashfs_directory,
        thread)
    if chroot_mount_points: unmount_mount_points(chroot_mount_points)

    # Attempt 2
    chroot_processes = get_processes_using_directory(custom_squashfs_directory)
    if chroot_processes: kill_processes(chroot_processes, model.terminal_pid)
    chroot_mount_points = get_mount_points_in_directory(
        custom_squashfs_directory,
        thread)
    if chroot_mount_points: unmount_mount_points(chroot_mount_points)

    #
    # Check if all chroot processes were killed.
    #
    chroot_processes = get_processes_using_directory(custom_squashfs_directory)
    if chroot_processes:
        logger.log_data('Error killing all chroot processes')
        for index, process in enumerate(chroot_processes):
            logger.log_data('Process % 2i.' % (index + 1), process)

    #
    # Check if all chroot mount points were unmounted.
    #
    chroot_mount_points = get_mount_points_in_directory(
        custom_squashfs_directory,
        thread)
    if chroot_mount_points:
        logger.log_data('Error unmounting all chroot mount points')
        for index, mount_point in enumerate(chroot_mount_points):
            logger.log_data('Mount point % 2i' % (index + 1), mount_point)

    # TODO: Consider using Python methods to remove this file.
    # Remove file /var/lib/dbus/machine-id.
    #
    # Since machine-id is no longer created in function
    # prepare_chroot_environment(), no need to delete it.
    '''
    command = 'rm -f "%s"' % os.path.join(
        custom_squashfs_directory,
        'var',
        'lib',
        'dbus',
        'machine-id')
    execute_synchronous(command, thread)
    '''
    # Turns off acccess control (all remote hosts will have access to X
    # server).
    # Turns access control back on (all remote hosts will not have
    # access to X server).
    # Removed xhost for bug #1766374
    # command = 'xhost -local:'
    # execute_synchronous(command, thread)


########################################################################
# Manage Linux Kernels Functions
########################################################################

# ------------------------------------------------------------------------------
# Kernel Versions
# ------------------------------------------------------------------------------


def create_kernel_details_list(*directories):
    logger.log_note('Create kernel details list')

    # Create a consolidated kernel details list.
    kernel_details_list = []
    for directory in directories:
        directory = os.path.realpath(directory)
        update_kernel_details_list_for_vmlinuz(directory, kernel_details_list)
        update_kernel_details_list_for_initrd(directory, kernel_details_list)

    # The resulting kernel_details is:
    # 0: version_integers
    # 1: version_name
    # 2: vmlinuz_filename
    # 3: new_vmlinuz_filename
    # 4: initrd_filename
    # 5: new_initrd_filename
    # 6: directory
    # 7: note
    # 8: is_selected
    # 9: is_remove

    # For debugging.
    # print_kernel_details_list(kernel_details_list)

    # total = len(kernel_details_list)
    # for index, kernel_details in enumerate(kernel_details_list):
    #     logger.log_data('version', kernel_details[0])
    #     logger.log_data('version', kernel_details[1])
    #     logger.log_data('• Index', '%s of %s' % (index, total - 1))
    #     logger.log_data('• Vmlinuz filename', kernel_details[2])
    #     logger.log_data('• New vmlinuz filename', kernel_details[3])
    #     logger.log_data('• Initrd filename', kernel_details[4])
    #     logger.log_data('• New initrd filename', kernel_details[5])
    #     logger.log_data('• Directory', kernel_details[6])
    #     logger.log_data('• Note', kernel_details[7])
    #     logger.log_data('• Is selected', kernel_details[8])
    #     # logger.log_data('• Is remove', kernel_details[9]

    # Remove kernels that do not have both vmlinuz filename and initrd filename.
    kernel_details_list = [
        kernel_details for kernel_details in kernel_details_list
        if kernel_details[2] and kernel_details[4]
    ]

    # For debugging.
    # print_kernel_details_list(kernel_details_list)

    # total = len(kernel_details_list)
    # for index, kernel_details in enumerate(kernel_details_list):
    #     logger.log_data('version', kernel_details[0])
    #     logger.log_data('version', kernel_details[1])
    #     logger.log_data('• Index', '%s of %s' % (index, total - 1))
    #     logger.log_data('• Vmlinuz filename', kernel_details[2])
    #     logger.log_data('• New vmlinuz filename', kernel_details[3])
    #     logger.log_data('• Initrd filename', kernel_details[4])
    #     logger.log_data('• New initrd filename', kernel_details[5])
    #     logger.log_data('• Directory', kernel_details[6])
    #     logger.log_data('• Note', kernel_details[7])
    #     logger.log_data('• Is selected', kernel_details[8])
    #     # logger.log_data('• Is remove', kernel_details[9]

    # Reverse sort the kernel details list by kernel version number (1st column).
    kernel_details_list.sort(
        key=lambda list: ['' if value is None else value for value in list],
        reverse=True)

    # Set the new vmlinuz filename.
    # Set the new initrd filename.
    for kernel_details in kernel_details_list:
        directory = kernel_details[6]
        vmlinuz_filename = kernel_details[2]
        vmlinuz_filepath = os.path.join(directory, vmlinuz_filename)
        new_vmlinuz_filename = calculate_vmlinuz_filename(vmlinuz_filepath)
        kernel_details[3] = new_vmlinuz_filename
        initrd_filename = kernel_details[4]
        initrd_filepath = os.path.join(directory, initrd_filename)
        new_initrd_filename = calculate_initrd_filename(initrd_filepath)
        kernel_details[5] = new_initrd_filename

    # Set the selected index as the index of the most recent kernel.
    selected_index = 0

    # Set the notes, and update the selected index if necessary.
    current_kernel_release_name = get_current_kernel_release_name()
    current_kernel_version_name = get_current_kernel_version_name()
    original_iso_image_directory = os.path.join(
        model.original_iso_image_mount_point,
        model.casper_relative_directory)
    for index, kernel_details in enumerate(kernel_details_list):
        note = ''
        version_name = kernel_details[1]
        if current_kernel_version_name == version_name:
            if note: note += ' '  # os.linesep
            note += 'This is the kernel version you are currently running.'
        if index == 0:
            if note: note += ' '  # os.linesep
            note += 'This is the newest kernel version that may be used to bootstrap the customized live ISO image.'
        directory = kernel_details[6]
        if directory == original_iso_image_directory:
            if note: note += ' '  # os.linesep
            note += 'This kernel is used to bootstrap the original live ISO image.'
            if len(kernel_details_list) > 1:
                if note: note += ' '  # os.linesep
                note += 'Select this kernel if you encounter issues such as BusyBox when using other kernel versions.'
            # if is_server_image()
            #     # if note: note += ' ' # os.linesep
            #     # note += 'Since you are customizing a server image, select this option if you encounter issues using other kernel versions.'
            #     # Set the selected index for the the original live ISO image kernel.
            #     selected_index = index
        new_vmlinuz_filename = kernel_details[3]
        new_initrd_filename = kernel_details[5]
        if note: note += ' '  # os.linesep
        note += 'Reference these files as <tt>%s</tt> and <tt>%s</tt> in the ISO boot configurations.' % (
            new_vmlinuz_filename,
            new_initrd_filename)
        kernel_details[7] = note

    # For debugging.
    print_kernel_details_list(kernel_details_list)

    # Set the selected kernel based on the selected index.
    kernel_details_list[selected_index][8] = True

    # Remove the 1st column because it is a tuple and cannot be rendered.
    # The resulting kernel_details is:
    # 0: version_name
    # 1: vmlinuz_filename
    # 2: new_vmlinuz_filename
    # 3: initrd_filename
    # 4: new_initrd_filename
    # 5: directory
    # 6: note
    # 7: is_selected
    # 8: is_remove
    [kernel_details.pop(0) for kernel_details in kernel_details_list]

    # Log the resuting list of kernel versions.
    total = len(kernel_details_list)
    for index, kernel_details in enumerate(kernel_details_list):
        logger.log_data('version', kernel_details[0])
        logger.log_data('• Index', '%s of %s' % (index, total - 1))
        logger.log_data('• Vmlinuz filename', kernel_details[1])
        logger.log_data('• New vmlinuz filename', kernel_details[2])
        logger.log_data('• Initrd filename', kernel_details[3])
        logger.log_data('• New initrd filename', kernel_details[4])
        logger.log_data('• Directory', kernel_details[5])
        logger.log_data('• Note', kernel_details[6])
        logger.log_data('• Is selected', kernel_details[7])
        # logger.log_data('• Is remove', kernel_details[8])

    return kernel_details_list


# For debugging only.
def print_kernel_details_list(kernel_details_list):
    total = len(kernel_details_list)
    for index, kernel_details in enumerate(kernel_details_list):
        print_kernel_details(kernel_details, index, total)


# For debugging only.
def print_kernel_details(kernel_details, index, total):
    print(
        '| '
        '{:13.13s} | '
        '{:8.8s} | '
        '{:6.6s} | '
        'Vmlinuz: {:15.15s} | '
        'New: {:15.15s} | '
        'Initrd: {:15.15s} | '
        'New: {:15.15s} | '
        'Directory: {:50.50s} | '
        'Note: {:5.5s} | '
        'Selected: {:5.5s} | '
        'Remove: {:5.5s} | '.format(
            str(kernel_details[0]),
            str(kernel_details[1]),
            '%s of %s' % (index,
                          total - 1),
            str(kernel_details[2]),
            str(kernel_details[3]),
            str(kernel_details[4]),
            str(kernel_details[5]),
            str(kernel_details[6]),
            str(kernel_details[7]),
            str(kernel_details[8]),
            str(kernel_details[9])))


def get_current_kernel_version_name():
    version_name = None
    try:
        version_information = re.search(
            r'(\d+\.\d+\.\d+(?:-\d+))',
            platform.release())
        version_name = version_information.group(1)
    except AttributeError as exception:
        pass

    return version_name


def get_current_kernel_release_name():
    return platform.release()


def is_server_image():
    # Guess if we are customizing a server image by checking the file
    # name, volume id, or disk name. For example:
    # - original_iso_image_filename = ubuntu-18.04-live-server-amd64.iso
    # - original_iso_image_volume_id = Ubuntu-Server 18.04 LTS amd64
    # - original_iso_image_disk_name = Ubuntu-Server 18.04 LTS "Bionic Beaver" - Release amd64

    if re.search('server', model.original_iso_image_filename, re.IGNORECASE):
        return True
    if re.search('server', model.original_iso_image_volume_id, re.IGNORECASE):
        return True
    if re.search('server', model.original_iso_image_disk_name, re.IGNORECASE):
        return True

    return False


# ------------------------------------------------------------------------------
# Vmlinuz
# ------------------------------------------------------------------------------


def update_kernel_details_list_for_vmlinuz(directory, kernel_details_list):

    logger.log_note('Update kernel details list for vmlinuz')
    filepath_pattern = os.path.join(directory, 'vmlinuz*')
    # Exclude broken symlinks.
    vmlinuz_filepath_list = [
        vmlinuz_filepath for vmlinuz_filepath in glob.glob(filepath_pattern)
        if os.path.exists(vmlinuz_filepath)
    ]
    logger.log_data(
        '%i vmlinuz files found in' % len(vmlinuz_filepath_list),
        directory)
    for vmlinuz_filepath in vmlinuz_filepath_list:
        vmlinuz_filename = os.path.basename(vmlinuz_filepath)
        logger.log_note('Get vmlinuz version details')
        version_name = get_vmlinuz_version_name(vmlinuz_filepath)
        if not version_name: version_name = '0.0.0-0'
        logger.log_data('The vmlinuz version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_vmlinuz(
            version_integers,
            version_name,
            vmlinuz_filename,
            directory,
            kernel_details_list)


def update_kernel_details_list_for_vmlinuz_EXPERIMENT(
        directory,
        kernel_details_list):

    logger.log_note('Update kernel details list for vmlinuz')
    filepath_pattern = os.path.join(directory, 'vmlinuz*')
    # vmlinuz_filepath_list = glob.glob(filepath_pattern)
    # vmlinuz_filepath_list = [ vmlinuz_filepath for vmlinuz_filepath in vmlinuz_filepath_list if os.path.exists(vmlinuz_filepath) ]
    vmlinuz_filepath_list = [
        vmlinuz_filepath for vmlinuz_filepath in glob.glob(filepath_pattern)
        if os.path.exists(vmlinuz_filepath)
    ]
    logger.log_data(
        '%i vmlinuz files found in' % len(vmlinuz_filepath_list),
        directory)
    for vmlinuz_filepath in vmlinuz_filepath_list:
        vmlinuz_filename = os.path.basename(vmlinuz_filepath)
        logger.log_note('Get vmlinuz version details')
        version_name = get_vmlinuz_version_name(vmlinuz_filepath)
        if not version_name: version_name = '0.0.0-0'
        logger.log_data('The vmlinuz version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_vmlinuz(
            version_integers,
            version_name,
            vmlinuz_filename,
            directory,
            kernel_details_list)


def update_kernel_details_list_for_vmlinuz_ORIGINAL(
        directory,
        kernel_details_list):

    logger.log_note('Update kernel details list for vmlinuz')
    filepath_pattern = os.path.join(directory, 'vmlinuz*')
    vmlinuz_filepath_list = glob.glob(filepath_pattern)
    logger.log_data(
        '%i vmlinuz files found in' % len(vmlinuz_filepath_list),
        directory)
    for vmlinuz_filepath in vmlinuz_filepath_list:
        vmlinuz_filename = os.path.basename(vmlinuz_filepath)
        logger.log_note('Get vmlinuz version details')
        version_name = get_vmlinuz_version_name(vmlinuz_filepath)
        if not version_name: version_name = '0.0.0-0'
        logger.log_data('The vmlinuz version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_vmlinuz(
            version_integers,
            version_name,
            vmlinuz_filename,
            directory,
            kernel_details_list)


def update_kernel_details_for_vmlinuz(
        version_integers,
        version_name,
        vmlinuz_filename,
        directory,
        kernel_details_list):

    logger.log_note('Search kernel details list for matching version')
    logger.log_data('• Kernel version', version_name)
    logger.log_data('• Kernel version as integers', version_integers)
    logger.log_data('• Vmlinuz filename', vmlinuz_filename)
    logger.log_data('• Directory', directory)

    # 0: version_integers
    # 1: version_name
    # 2: vmlinuz_filename
    # 3: new_vmlinuz_filename
    # 4: initrd_filename
    # 5: new_initrd_filename
    # 6: directory
    # 7: note
    # 8: is_selected
    # 9: is_remove

    found = False
    for index, kernel_details in enumerate(list(kernel_details_list)):
        if (kernel_details[0] == version_integers
                and kernel_details[1] == version_name
                and kernel_details[6] == directory):
            found = True
            if kernel_details[2] == vmlinuz_filename:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Skip updating kernel details')

                logger.log_data('• Index', '%s of %s' % (index, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
                break  # TODO: break is not needed here.
            elif not kernel_details[2]:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Update kernel details')
                kernel_details[2] = vmlinuz_filename

                logger.log_data('• Index', '%s of %s' % (index, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
            else:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Copy and add kernel details')
                kernel_details = list(kernel_details)
                kernel_details[2] = vmlinuz_filename
                kernel_details_list.append(kernel_details)

                total = len(kernel_details_list)
                logger.log_data('• Index', '%s of %s' % (total - 1, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
    if not found:
        logger.log_data('• Matching kernel version found?', 'No')

        logger.log_note('Add new kernel details')

        kernel_details = [None] * 10
        if not version_integers:
            version_integers = (0, 0, 0)
        kernel_details[0] = version_integers
        kernel_details[1] = version_name
        kernel_details[2] = vmlinuz_filename
        kernel_details[3] = None  # new_vmlinuz_filename
        kernel_details[4] = None  # initrd_filename
        kernel_details[5] = None  # new_initrd_filename
        kernel_details[6] = directory
        kernel_details[7] = None  # note
        kernel_details[8] = False  # is_selected
        kernel_details[9] = False  # is_remove
        kernel_details_list.append(kernel_details)

        total = len(kernel_details_list)
        logger.log_data('• Index', '%s of %s' % (total - 1, total - 1))
        logger.log_data('• Kernel version', kernel_details[1])
        logger.log_data('• Kernel version as integers', kernel_details[0])
        logger.log_data('• Vmlinuz filename', kernel_details[2])
        logger.log_data('• Initrd filename', kernel_details[4])
        logger.log_data('• Directory', kernel_details[6])


def get_vmlinuz_version_name(filepath):

    # logger.log_data('Get vmlinuz version', filepath)
    version_name = (
        _get_vmlinuz_version_name_from_file_name(filepath)
        or _get_vmlinuz_version_name_from_file_type(filepath)
        or _get_vmlinuz_version_name_from_file_contents(filepath))

    return version_name


def _get_vmlinuz_version_name_from_file_name(filepath):

    logger.log_data('Get vmlinuz version from file name', filepath)
    filename = os.path.basename(filepath)
    version_name = re.search(r'\d[\d\.-]*\d', filename)
    version_name = version_name.group(0) if version_name else None

    return version_name


def _get_vmlinuz_version_name_from_file_type(filepath):

    logger.log_data('Get vmlinuz version from file type', filepath)
    command = 'file "%s"' % filepath
    result, error = execute_synchronous(command)
    version_name = None
    if not error:
        version_information = re.search(
            r'(\d+\.\d+\.\d+(?:-\d+))',
            str(result))
        if version_information:
            version_name = version_information.group(1)
            logger.log_data('Found version', version_name)

    return version_name


def _get_vmlinuz_version_name_from_file_contents(filepath):

    logger.log_data('Get vmlinuz version from file contents', filepath)
    version_name = None
    with open(filepath, errors='ignore') as file:
        contents = file.read()
    candidate = ''
    for character in contents:
        if character in string.printable:
            candidate += character
        elif len(candidate) > 4:
            try:
                version_information = re.search(
                    r'(\d+\.\d+\.\d+(?:-\d+))',
                    str(candidate))
                version_name = version_information.group(1)
                logger.log_data('Found version', version_name)
                break
            except:
                candidate = ''
        else:
            candidate = ''

    return version_name


# ------------------------------------------------------------------------------
# Initrd
# ------------------------------------------------------------------------------


def update_kernel_details_list_for_initrd(directory, kernel_details_list):

    logger.log_note('Update kernel details list for initrd')
    filepath_pattern = os.path.join(directory, 'initrd*')
    # Exclude broken symlinks.
    initrd_filepath_list = [
        initrd_filepath for initrd_filepath in glob.glob(filepath_pattern)
        if os.path.exists(initrd_filepath)
    ]
    logger.log_data(
        '%i initrd files found in' % len(initrd_filepath_list),
        directory)
    for initrd_filepath in initrd_filepath_list:
        initrd_filename = os.path.basename(initrd_filepath)
        logger.log_note('Get initrd version details')
        version_name = get_initrd_version_name(initrd_filepath)

        # TODO: See if this hack can be improved?
        # As a last resort, grab the first vmlinuz version from this
        # directory, and assume the initrd version is the same. The
        # situation where the initrd version is unknown should only
        # happen in the casper directory of the ISO; this is a critical
        # assumption. In the casper directory, the initrd version should
        # correspond to the vmlinuz version, and it is reasonable to
        # simply use the vmlinuz version, whenever the version of initrd
        # cannot be determined in this directory.
        if not version_name:
            version_name = get_vmlinuz_version_from_kernel_details_list(
                kernel_details_list,
                directory)

        logger.log_data('The initrd version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_initrd(
            version_integers,
            version_name,
            initrd_filename,
            directory,
            kernel_details_list)


def get_vmlinuz_version_from_kernel_details_list(
        kernel_details_list,
        directory):

    # The kernel_details is:
    # 0: version_integers
    # 1: version_name
    # 2: vmlinuz_filename
    # 3: new_vmlinuz_filename
    # 4: initrd_filename
    # 5: new_initrd_filename
    # 6: directory
    # 7: note
    # 8: is_selected
    # 9: is_remove

    version_name = '0.0.0-0'
    for kernel_details in kernel_details_list:
        if directory == kernel_details[6]:
            version_name = kernel_details[1]
            break
    return version_name


def update_kernel_details_list_for_initrd_EXPERIMENT(
        directory,
        kernel_details_list):

    logger.log_note('Update kernel details list for initrd')
    filepath_pattern = os.path.join(directory, 'initrd*')
    # initrd_filepath_list = glob.glob(filepath_pattern)
    # initrd_filepath_list = [ initrd_filepath for initrd_filepath in initrd_filepath_list if not os.path.exists(initrd_filepath) ]
    initrd_filepath_list = [
        initrd_filepath for initrd_filepath in glob.glob(filepath_pattern)
        if os.path.exists(initrd_filepath)
    ]
    logger.log_data(
        '%i initrd files found in' % len(initrd_filepath_list),
        directory)
    for initrd_filepath in initrd_filepath_list:
        initrd_filename = os.path.basename(initrd_filepath)
        logger.log_note('Get initrd version details')
        version_name = get_initrd_version_name(initrd_filepath)
        if not version_name: version_name = '0.0.0-0'
        logger.log_data('The initrd version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_initrd(
            version_integers,
            version_name,
            initrd_filename,
            directory,
            kernel_details_list)


def update_kernel_details_list_for_initrd_ORIGINAL(
        directory,
        kernel_details_list):

    logger.log_note('Update kernel details list for initrd')
    filepath_pattern = os.path.join(directory, 'initrd*')
    initrd_filepath_list = glob.glob(filepath_pattern)
    logger.log_data(
        '%i initrd files found in' % len(initrd_filepath_list),
        directory)
    for initrd_filepath in initrd_filepath_list:
        initrd_filename = os.path.basename(initrd_filepath)
        logger.log_note('Get initrd version details')
        version_name = get_initrd_version_name(initrd_filepath)
        if not version_name: version_name = '0.0.0-0'
        logger.log_data('The initrd version is', version_name)
        version_integers = tuple(map(int, re.split('[.-]', version_name)))
        update_kernel_details_for_initrd(
            version_integers,
            version_name,
            initrd_filename,
            directory,
            kernel_details_list)


def update_kernel_details_for_initrd(
        version_integers,
        version_name,
        initrd_filename,
        directory,
        kernel_details_list):

    logger.log_note('Search kernel details list for matching version')
    logger.log_data('• Kernel version', version_name)
    logger.log_data('• Kernel version as integers', version_integers)
    logger.log_data('• Initrd filename', initrd_filename)
    logger.log_data('• Directory', directory)

    # 0: version_integers
    # 1: version_name
    # 2: vmlinuz_filename
    # 3: new_vmlinuz_filename
    # 4: initrd_filename
    # 5: new_initrd_filename
    # 6: directory
    # 7: note
    # 8: is_selected
    # 9: is_remove

    found = False
    for index, kernel_details in enumerate(list(kernel_details_list)):
        if (kernel_details[0] == version_integers
                and kernel_details[1] == version_name
                and kernel_details[6] == directory):
            found = True
            if kernel_details[4] == initrd_filename:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Skip updating kernel details')

                logger.log_data('• Index', '%s of %s' % (index, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
                break  # TODO: break is not needed here.
            elif not kernel_details[4]:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Update kernel details')
                kernel_details[4] = initrd_filename

                logger.log_data('• Index', '%s of %s' % (index, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
            else:
                logger.log_data('• Matching kernel version found?', 'Yes')
                total = len(kernel_details_list)
                logger.log_data(
                    '• Index of match',
                    '%i of %i' % (index,
                                  total - 1))

                logger.log_note('Copy and add kernel details')
                kernel_details = list(kernel_details)
                kernel_details[4] = initrd_filename
                kernel_details_list.append(kernel_details)

                total = len(kernel_details_list)
                logger.log_data('• Index', '%s of %s' % (total - 1, total - 1))
                logger.log_data('• Kernel version', kernel_details[1])
                logger.log_data(
                    '• Kernel version as integers',
                    kernel_details[0])
                logger.log_data('• Vmlinuz filename', kernel_details[2])
                logger.log_data('• Initrd filename', kernel_details[4])
                logger.log_data('• Directory', kernel_details[6])
    if not found:
        logger.log_data('• Matching kernel version found?', 'No')

        logger.log_note('Add new kernel details')

        kernel_details = [None] * 10
        if not version_integers:
            version_integers = (0, 0, 0)
        kernel_details[0] = version_integers
        kernel_details[1] = version_name
        kernel_details[2] = None  # vmlinuz_filename
        kernel_details[3] = None  # new_vmlinuz_filename
        kernel_details[4] = initrd_filename
        kernel_details[5] = None  # new_initrd_filename
        kernel_details[6] = directory
        kernel_details[7] = None  # note
        kernel_details[8] = False  # is_selected
        kernel_details[9] = False  # is_remove
        kernel_details_list.append(kernel_details)

        total = len(kernel_details_list)
        logger.log_data('• Index', '%s of %s' % (total - 1, total - 1))
        logger.log_data('• Kernel version', kernel_details[1])
        logger.log_data('• Kernel version as integers', kernel_details[0])
        logger.log_data('• Vmlinuz filename', kernel_details[2])
        logger.log_data('• Initrd filename', kernel_details[4])
        logger.log_data('• Directory', kernel_details[6])


def get_initrd_version_name(filepath):

    # logger.log_data('Get initrd version', filepath)
    version_name = (
        _get_initrd_version_name_from_file_name(filepath)
        or _get_initrd_version_name_from_file_contents(filepath)
        or _get_initrd_version_name_from_file_type(filepath))

    return version_name


def _get_initrd_version_name_from_file_name(filepath):

    logger.log_data('Get initrd version from file name', filepath)
    filename = os.path.basename(filepath)
    version_name = re.search(r'\d[\d\.-]*\d', filename)
    version_name = version_name.group(0) if version_name else None

    return version_name


def _get_initrd_version_name_from_file_type(filepath):

    logger.log_data('Get initrd version from file type', filepath)
    command = 'file "%s"' % filepath
    result, error = execute_synchronous(command)
    version_name = None
    if not error:
        version_information = re.search(
            r'(\d+\.\d+\.\d+(?:-\d+))',
            str(result))
        if version_information:
            version_name = version_information.group(1)
            logger.log_data('Found version', version_name)

    return version_name


def _get_initrd_version_name_from_file_contents(filepath):

    logger.log_data('Get initrd version from file contents', filepath)
    version_name = None
    try:
        command = 'lsinitramfs "%s"' % filepath
        process = pexpect.spawnu(command, timeout=60)
        match = False
        while process.exitstatus is None and not match:
            line = process.readline()
            # print('%s' % line, end='')
            match = re.search(r'lib/modules/(\d[\d\.-]*\d)', line)
            if ('cannot' in line or 'error' in line or 'premature' in line):
                logger.log_data(
                    'Encountered exception while getting initrd version from file contents',
                    line)
        if match:
            process.terminate(True)
            version_name = match.group(1)
    except pexpect.TIMEOUT as exception:
        logger.log_data(
            'Encountered exception while getting initrd version from file contents',
            exception)
    except pexpect.EOF as exception:
        logger.log_data(
            'Encountered exception while getting initrd version from file contents',
            exception)
    except pexpect.ExceptionPexpect as exception:
        logger.log_data(
            'Encountered exception while getting initrd version from file contents',
            exception)

    return version_name


########################################################################
# Create Filesystem Manifest Functions
########################################################################


def is_exists_filesystem_manifest_remove(filename):

    # Check custom live iso directory
    directory = os.path.realpath(model.custom_live_iso_directory)
    filepath = os.path.join(
        directory,
        model.casper_relative_directory,
        filename)

    is_exists = os.path.exists(filepath)
    if is_exists:
        logger.log_data(
            '%s found in' % filename,
            os.path.join(directory,
                         model.casper_relative_directory))
        return True
    else:
        logger.log_data(
            '%s not found in' % filename,
            os.path.join(directory,
                         model.casper_relative_directory))
        return False


def create_installed_packages_list(thread):

    logger.log_note('Create list of installed packages')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    # command = 'chroot "%s" dpkg-query -W' % custom_squashfs_directory
    # command = 'chroot "%s" dpkg-query --showformat="${Package}\t${Version}\n" --show' % custom_squashfs_directory
    command = 'chroot "%s" dpkg-query --show' % custom_squashfs_directory
    ## execute_asynchronous(command, thread)
    ## output = thread.process.read()
    result, error = execute_synchronous(command, thread)
    installed_packages_list = result.splitlines()

    package_count = len(installed_packages_list)
    logger.log_data('Total number of installed packages', package_count)

    return installed_packages_list


def create_filesystem_manifest_file(installed_packages_list):

    logger.log_note('Create new filesystem manifest file')

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    filepath = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        'filesystem.manifest')
    logger.log_data('Write filesystem manifest to', filepath)
    with open(filepath, 'w') as file:
        for line in installed_packages_list:
            file.write('%s\n' % line)


def get_removable_packages_list(filename):

    # Read filesystem.manifest-remove to get list of packages to remove.
    removable_packages_list = []
    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    filepath = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        filename)
    logger.log_data('Read list of packages to remove from', filepath)
    with open(filepath, 'r') as file:
        removable_packages_list = file.read().splitlines()

    return removable_packages_list


def create_package_details_list(
        installed_packages_list,
        removable_packages_list_1,
        removable_packages_list_2):
    logger.log_note('Create package details list')

    # List installed packages and mark packages that will be removed.

    number_of_packages_to_remove_1 = 0
    number_of_packages_to_retain_1 = 0
    number_of_packages_to_remove_2 = 0
    number_of_packages_to_retain_2 = 0
    package_details_list = []

    for line in installed_packages_list:

        package_details = line.split()
        package_name = package_details[0]

        # Somme package names in installed_packages_list specify the
        # architecture suffix (ex. gir1.2-rb-3.0:amd64).
        # However, removable_packages_list may or may not contain
        # packages with the architectre suffix (ex. gir1.2-rb-3.0).
        # • filesystem.manifest-remove lists packages with the
        #   architectre suffix.
        # • filesystem.manifest-minimal-remove lists packages without
        #   the architectre suffix.
        # Therefore, check the package name with and without the
        # architectre suffix.

        is_remove_1 = (package_name in removable_packages_list_1) or (
            package_name.rpartition(':')[0] in removable_packages_list_1)
        number_of_packages_to_remove_1 += is_remove_1
        number_of_packages_to_retain_1 += not is_remove_1

        is_remove_2 = (package_name in removable_packages_list_2) or (
            package_name.rpartition(':')[0] in removable_packages_list_2)
        number_of_packages_to_remove_2 += is_remove_2
        number_of_packages_to_retain_2 += not is_remove_2

        # Insert columns at the beginning of package_details to indicate if the
        # package_name should be removed (True) or kept (False).

        # Set typical checkbutton selected or unselected
        package_details.insert(0, is_remove_1)
        # Set minimal checkbutton selected or unselected
        package_details.insert(1, is_remove_2 or is_remove_1)
        # Backup original minimal checkbutton value
        package_details.insert(2, is_remove_2)
        # Set minimal checkbutton active or inactive
        package_details.insert(3, not is_remove_1)

        package_details_list.append(package_details)

    logger.log_data(
        'Total number of installed packages',
        len(installed_packages_list))
    logger.log_data(
        'Number of packages to be removed after a typical install',
        number_of_packages_to_remove_1)
    logger.log_data(
        'Number of packages to be retained after a typical install',
        number_of_packages_to_retain_1)
    logger.log_data(
        'Number of packages to be removed after a minimal install',
        number_of_packages_to_remove_2)
    logger.log_data(
        'Number of packages to be retained after a minimal install',
        number_of_packages_to_retain_2)

    return package_details_list


def create_typical_removable_packages_list():
    logger.log_note('Create typical removable packages list')

    listore_name = 'options_page__package_manifest_tab__liststore'
    logger.log_data('Get user selections from', listore_name)
    liststore = model.builder.get_object(listore_name)
    removable_packages_list = []
    item = liststore.get_iter_first()
    while item is not None:
        flag = liststore.get_value(item, 0)
        package_name = liststore.get_value(item, 4)
        if flag: removable_packages_list.append(package_name)
        item = liststore.iter_next(item)
    removable_packages_list
    logger.log_data(
        'New number of packages to be removed',
        len(removable_packages_list))

    return removable_packages_list


def create_minimal_removable_packages_list():
    logger.log_note('Create minimal removable packages list')

    listore_name = 'options_page__package_manifest_tab__liststore'
    logger.log_data('Get user selections from', listore_name)
    liststore = model.builder.get_object(listore_name)
    removable_packages_list = []
    item = liststore.get_iter_first()
    while item is not None:
        flag = liststore.get_value(item, 1) and liststore.get_value(item, 3)
        package_name = liststore.get_value(item, 4)
        if flag: removable_packages_list.append(package_name)
        item = liststore.iter_next(item)
    removable_packages_list
    logger.log_data(
        'New number of packages to be removed',
        len(removable_packages_list))

    return removable_packages_list


# TODO: This function is not used.
def create_removable_packages_list(listore_name, index):
    logger.log_note('Get removable packages list from user selections')
    logger.log_data('Get user selections from', listore_name)
    liststore = model.builder.get_object(listore_name)
    removable_packages_list = []
    item = liststore.get_iter_first()
    while item is not None:
        flag = liststore.get_value(item, index)
        package_name = liststore.get_value(item, 2)
        if flag: removable_packages_list.append(package_name)
        item = liststore.iter_next(item)
    removable_packages_list
    logger.log_data(
        'New number of packages to be removed',
        len(removable_packages_list))

    return removable_packages_list


def create_filesystem_manifest_remove_file(filename, removable_packages_list):
    logger.log_note('Create new filesystem manifest remove file')

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    filepath = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        filename)
    logger.log_data('Write filesystem manifest remove file to', filepath)
    with open(filepath, 'w') as file:
        first_line = True
        for packages_name in removable_packages_list:
            if first_line:
                file.write('%s' % packages_name)
                first_line = False
            else:
                file.write('\n%s' % packages_name)


########################################################################
# Repackage Functions
########################################################################


def save_stack_buffers(stack_name):

    stack = model.builder.get_object(stack_name)
    scrolled_windows = stack.get_children()

    for scrolled_window in scrolled_windows:

        filepath = stack.child_get_property(scrolled_window, 'name')
        title = stack.child_get_property(scrolled_window, 'title')

        logger.log_data('Write file', filepath)

        # Get the updated text.
        source_view = scrolled_window.get_child()
        source_buffer = source_view.get_buffer()
        start_iter = source_buffer.get_start_iter()
        end_iter = source_buffer.get_end_iter()
        data = source_buffer.get_text(start_iter, end_iter, True)

        # Create the parent directories (/preseed, /boot/grub, /isolinux, etc.)
        # if they do not exist.
        directory = os.path.dirname(filepath)
        os.makedirs(directory, exist_ok=True)
        os.chmod(
            directory,
            stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR
            | stat.S_IXGRP | stat.S_IXOTH)

        # Write the file.
        with open(filepath, 'w') as file:
            file.write(data)
        # file.flush()
        os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


# TODO: Remove this function when 14.04 is no longer supported.
# This function is necessary because Gtk 3.10 in Ubuntu 14.04 does not support
# Gtk.Stack or Gtk.StackSidebar.
# This function identifies the selected kernel, then replaces text in the boot
# configurations based on this selection.
def update_and_save_boot_configurations():

    logger.log_data('Update boot configurations for Ubuntu 14.04')

    # Get the selected kernel details.
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
    for selected_index, kernel_details in enumerate(liststore):
        if kernel_details[7]: break
    else: selected_index = 0
    logger.log_data('The selected kernel is index number', selected_index)

    # Search and replace text.
    search_text_1 = r'/vmlinuz\S*'
    replacement_text_1 = '/%s' % liststore[selected_index][2]
    search_text_2 = r'/initrd\S*'
    replacement_text_2 = '/%s' % liststore[selected_index][4]

    # Update grub.cfg.
    filepath = os.path.join(
        model.custom_live_iso_directory,
        'boot',
        'grub',
        'grub.cfg')
    replace_text_in_file(filepath, search_text_1, replacement_text_1)
    replace_text_in_file(filepath, search_text_2, replacement_text_2)
    if os.path.exists(filepath):
        os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    # Update loopback.cfg.
    filepath = os.path.join(
        model.custom_live_iso_directory,
        'boot',
        'grub',
        'loopback.cfg')
    replace_text_in_file(filepath, search_text_1, replacement_text_1)
    replace_text_in_file(filepath, search_text_2, replacement_text_2)
    if os.path.exists(filepath):
        os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    '''
        # Update isolinux.cfg.
        filepath = os.path.join(model.custom_live_iso_directory, 'isolinux', 'isolinux.cfg')
        replace_text_in_file(filepath, search_text_1, replacement_text_1)
        replace_text_in_file(filepath, search_text_2, replacement_text_2)
        if os.path.exists(filepath): os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        '''

    # Update txt.cfg.
    filepath = os.path.join(
        model.custom_live_iso_directory,
        'isolinux',
        'txt.cfg')
    replace_text_in_file(filepath, search_text_1, replacement_text_1)
    replace_text_in_file(filepath, search_text_2, replacement_text_2)
    if os.path.exists(filepath):
        os.chmod(filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def copy_vmlinuz_and_initrd_files(thread):

    logger.log_note('Update ISO boot files')

    # Get the selected kernel details.
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
    for selected_index, kernel_details in enumerate(liststore):
        if kernel_details[7]: break
    else: selected_index = 0
    logger.log_data('The selected kernel is index number', selected_index)

    # Get selected directory.
    # source_directory = os.path.realpath(liststore[selected_index][5])
    source_directory = liststore[selected_index][5]

    # Get target directory.
    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    target_directory = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory)

    #
    # vmlinuz
    #

    # Delete existing vmlinuz* file(s) in target directory.
    pattern = os.path.join(target_directory, 'vmlinuz*')
    delete_files_with_pattern(pattern)

    # Get selected vmlinuz filepath.
    source_filepath = os.path.join(
        source_directory,
        liststore[selected_index][1])

    # Get target vmlinuz filepath.
    target_filename = liststore[selected_index][2]
    target_filepath = os.path.join(target_directory, target_filename)

    # Copy selected vmlinuz* file to target directory.
    copy_boot_file(source_filepath, 0, target_filepath, 2, thread)
    # $ chmod a=r ./custom-live-iso/casper/vmlinuz{.???}
    # $ chmod a=r ./custom-live-iso/install/vmlinuz{.???} (ex. ubuntu-14.04.5-server-amd64.iso)
    os.chmod(
        target_filepath,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    #
    # initrd
    #

    # Delete existing initrd* file in target directory
    pattern = os.path.join(target_directory, 'initrd*')
    delete_files_with_pattern(pattern)

    # Get selected initrd filepath.
    source_filepath = os.path.join(
        source_directory,
        liststore[selected_index][3])

    # Get target initrd filepath.
    target_filename = liststore[selected_index][4]
    target_filepath = os.path.join(target_directory, target_filename)

    # Copy selected initrd* file to target directory
    copy_boot_file(source_filepath, 1, target_filepath, 2, thread)
    # $ chmod a=r ./custom-live-iso/casper/initrd{.???}
    # $ chmod a=r ./custom-live-iso/install/initrd{.???} (ex. ubuntu-14.04.5-server-amd64.iso)
    os.chmod(
        target_filepath,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)


#
# Create relative links
#

# TODO: Make sure the following *relative* links are created:
#       - squashfs-root/initrd.img --> /boot/initrd.img-4.8.0-37-generic
#       - squashfs-root/vmlinuz    --> /boot/vmlinuz-4.8.0-37-generic
#       - Use the function: os.symlink(src, dst)


def delete_files_with_pattern(pattern):
    logger.log_data('Delete existig  files with pattern', pattern)
    # TODO: Make this code more clear.
    [os.remove(delete_filepath) for delete_filepath in glob.glob(pattern)]


def calculate_vmlinuz_filename(filepath):

    # Just use vmlinuz (instead of vmlinuz or vmlinuz.efi).
    filename = 'vmlinuz'

    return filename


def calculate_initrd_filename(filepath):

    # Determine extension for initrd file.
    # Use initrd.lz, initrd.gz, or initrd depending on the compression type.
    command = 'file "%s"' % filepath
    result, error = execute_synchronous(command)
    logger.log_data('The file type informaton is', result)

    compression = None
    match = re.search(r':\s(.*)\scompressed data', result)
    if match: compression = match.group(1)
    else: logger.log_data('Compression for initrd not found in', filepath)
    logger.log_data('The compression for initrd is', compression)

    if compression == 'LZMA': filename = 'initrd.lz'
    elif compression == 'gzip': filename = 'initrd.gz'
    else: filename = 'initrd'

    return filename


def copy_boot_file(
        source_filepath,
        file_number,
        target_filepath,
        total_files,
        thread):
    logger.log_data(
        'Copy file',
        'Number %s of %s' % (file_number + 1,
                             total_files))
    logger.log_data('The source file is', source_filepath)
    logger.log_data('The target file is', target_filepath)

    command = 'rsync --archive --no-relative --no-implied-dirs --info=progress2 "%s" "%s"' % (
        source_filepath,
        target_filepath)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread)
    logger.log_data('• The start time is', formatted_time)

    progress_initial_global = int(round(100 * file_number / total_files, 0))

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):

        try:
            line = thread.process.read_nonblocking(100, 0.05)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(0.01)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'repackage_iso_page__copy_boot_files_progressbar',
                    None)
            display.update_progressbar_percent(
                'repackage_iso_page__copy_boot_files_progressbar',
                progress_initial_global + progress_display / total_files)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    time.sleep(0.01)


def create_squashfs(thread):

    _create_squashfs(thread)


def _create_squashfs_TESTING(thread):
    logger.log_note('Create squashfs (Testing)')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    source_path = custom_squashfs_directory
    logger.log_data('The source path is', source_path)

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    target_path = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        'filesystem.squashfs')
    logger.log_data('The target path is', target_path)


def _create_squashfs(thread):
    logger.log_note('Create squashfs')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    source_path = custom_squashfs_directory
    logger.log_data('The source path is', source_path)

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    target_path = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        'filesystem.squashfs')
    logger.log_data('The target path is', target_path)

    # https://catchchallenger.first-world.info/wiki/Quick_Benchmark:_Gzip_vs_Bzip2_vs_LZMA_vs_XZ_vs_LZ4_vs_LZO
    # command = 'mksquashfs "%s" "%s" -noappend -comp xz' % (
    #     source_path,
    #     target_path)

    # Optionally use gzip (lower compression) or xz (higher compression).
    ### TODO: Revert this to xz compression or add a page to select compression level.
    # command = 'mksquashfs "%s" "%s" -noappend -comp xz' % (
    #     source_path,
    #     target_path)
    #
    # command = 'mksquashfs "%s" "%s" -noappend -comp gzip' % (
    #     source_path,
    #     target_path)

    # Originally added etc/ssh/ssh_host*to resolve Bug #1824715.
    # Removed etc/ssh/ssh_host* due to Bug #1825566.
    # command = (
    #     'mksquashfs "%s" "%s"'
    #     ' -noappend'
    #     ' -comp gzip'
    #     ' -wildcards'
    #     ' -e "root/.bash_history"'
    #     ' -e "root/.cache"'
    #     ' -e "root/.wget-hsts"'
    #     ' -e "home/*/.bash_history"'
    #     ' -e "home/*/.cache"'
    #     ' -e "home/*/.wget-hsts"'
    #     ' -e "etc/ssh/ssh_host*"'
    #     ' -e "tmp/*"'
    #     ' -e "tmp/.*"' % (source_path,
    #                       target_path))

    command = (
        'mksquashfs "%s" "%s"'
        ' -noappend'
        ' -comp gzip'
        ' -wildcards'
        ' -e "root/.bash_history"'
        ' -e "root/.cache"'
        ' -e "root/.wget-hsts"'
        ' -e "home/*/.bash_history"'
        ' -e "home/*/.cache"'
        ' -e "home/*/.wget-hsts"'
        ' -e "tmp/*"'
        ' -e "tmp/.*"' % (source_path,
                          target_path))

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread)
    logger.log_data('• The start time is', formatted_time)

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):

        try:
            line = thread.process.read_nonblocking(100, 0.05)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(0.05)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'repackage_iso_page__create_squashfs_progressbar',
                    None)
            display.update_progressbar_percent(
                'repackage_iso_page__create_squashfs_progressbar',
                progress_display)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    time.sleep(0.10)


def update_filesystem_size(thread):
    logger.log_note('Update filesystem size')

    custom_squashfs_directory = os.path.realpath(
        model.custom_squashfs_directory)
    command = 'du --summarize --one-file-system --block-size=1 "%s"' % custom_squashfs_directory
    result, error = execute_synchronous(command, thread)
    size = '0'
    if not error:
        size_information = re.search(r'^([0-9]+)\s', result)
        if size_information:
            size = size_information.group(1)
        else:
            logger.log_data(
                'Unable to get filesystem size for %s' %
                custom_squashfs_directory,
                result)
    else:
        logger.log_data(
            'Unable to get filesystem size for %s' % custom_squashfs_directory,
            result)

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    filepath = os.path.join(
        custom_live_iso_directory,
        model.casper_relative_directory,
        'filesystem.size')
    logger.log_data('Write filesystem size to', filepath)
    with open(filepath, 'w') as file:
        file.write('%s' % size)

    return int(size)


def update_disk_name():
    logger.log_note('Update disk name')

    try:
        custom_live_iso_directory = os.path.realpath(
            model.custom_live_iso_directory)
        filepath = os.path.join(
            custom_live_iso_directory,
            'README.diskdefines')
        search_text = r'^#define DISKNAME.*'
        replacement_text = '#define DISKNAME %s' % model.custom_iso_image_disk_name
        logger.log_data('Write disk name to', filepath)
        replace_text_in_file(filepath, search_text, replacement_text)
    except Exception as exception:
        logger.log_data(
            'Ignoring exception while updating disk name in README.diskdefines',
            exception)


def update_disk_info():
    logger.log_note('Update disk information')

    try:
        custom_live_iso_directory = os.path.realpath(
            model.custom_live_iso_directory)
        filepath = os.path.join(custom_live_iso_directory, '.disk', 'info')
        current_time = datetime.datetime.now()
        formatted_time = '{:%Y%m%d}'.format(current_time)
        text = '%s (%s)' % (model.custom_iso_image_disk_name, formatted_time)
        logger.log_data(
            'Write custom ISO image disk name and release date',
            text)
        logger.log_data('Write to', filepath)
        with open(filepath, 'w') as file:
            file.write('%s' % text)
    except Exception as exception:
        logger.log_data(
            'Ignoring exception while updating disk name in .disk/info',
            exception)


def calculate_md5_hash_for_file(filepath, blocksize=2**20):
    # filepath = os.path.realpath(filepath)
    hash = hashlib.md5()
    with open(filepath, 'rb') as file:
        while True:
            buffer = file.read(blocksize)
            if not buffer: break
            hash.update(buffer)
    return hash.hexdigest()


def update_md5_checksums_WITHOUT_PROGRESS(
        checksums_filepath,
        start_directory,
        exclude_paths):
    logger.log_note('Update md5 sums')
    checksums_filepath = os.path.realpath(checksums_filepath)
    start_directory = os.path.realpath(start_directory)
    exclude_paths = [os.path.realpath(path) for path in exclude_paths]
    logger.log_data('Write md5 sums to', checksums_filepath)
    count = 0
    with open(checksums_filepath, 'w') as file:
        for directory, directory_names, filenames in os.walk(start_directory):
            if directory not in exclude_paths:
                for filename in filenames:
                    filepath = os.path.join(directory, filename)
                    if (filepath not in exclude_paths):
                        count += 1
                        hash = calculate_md5_hash_for_file(filepath)
                        relative_filepath = os.path.relpath(
                            filepath,
                            start_directory)
                        file.write('%s  ./%s\n' % (hash, relative_filepath))
                        # logger.log_note('%s  ./%s' % (hash, relative_filepath))
    return count


def update_md5_checksums(checksums_filepath, start_directory, exclude_paths):
    logger.log_note('Update MD5 checksums')
    checksums_filepath = os.path.realpath(checksums_filepath)
    start_directory = os.path.realpath(start_directory)
    exclude_paths = [os.path.realpath(path) for path in exclude_paths]
    logger.log_data('Write MD5 checksums to', checksums_filepath)

    # Get filepaths.
    filepaths = []
    for directory, directory_names, filenames in os.walk(start_directory):
        if directory not in exclude_paths:
            for filename in filenames:
                filepath = os.path.join(directory, filename)
                if (filepath not in exclude_paths):
                    filepaths.append(filepath)
    filepaths.sort(key=lambda filepath: filepath.lower())

    # Calculate MD5 checksums and display progress.
    file_number = 0
    total_files = len(filepaths)
    with open(checksums_filepath, 'w') as file:
        for filepath in filepaths:
            file_number += 1
            display.update_progressbar_text(
                'repackage_iso_page__update_checksums_progressbar',
                'Calculating checksum for file %i of %i' %
                (file_number,
                 total_files))
            hash = calculate_md5_hash_for_file(filepath)
            relative_filepath = os.path.relpath(filepath, start_directory)
            file.write('%s  ./%s\n' % (hash, relative_filepath))
            # logger.log_note('%s  ./%s' % (hash, relative_filepath))
            display.update_progressbar_percent(
                'repackage_iso_page__update_checksums_progressbar',
                100 * file_number / total_files)
            time.sleep(0.01)

    return total_files


def count_lines(filepath, thread):
    # filepath = os.path.realpath(filepath)
    command = 'wc --lines "%s"' % filepath
    ## execute_asynchronous(command, thread)
    ## line = thread.process.read()
    result, error = execute_synchronous(command, thread)
    count = 0
    if not error:
        count_information = re.search(r'([0-9]*) ', str(result))
        if count_information:
            count = count_information.group(1)
        else:
            logger.log_data('Unable to count lines for %s' % filepath, result)
    else:
        logger.log_data('Unable to count lines for %s' % filepath, result)

    return int(count)


def create_iso_image(thread):

    logger.log_note('Create ISO image')

    custom_live_iso_directory = os.path.realpath(
        model.custom_live_iso_directory)
    efi_image_filepath = os.path.join(
        custom_live_iso_directory,
        'boot/grub/efi.img')

    custom_iso_image_filepath = os.path.realpath(
        model.custom_iso_image_filepath)

    # Bug #1623261
    # https://www.gnu.org/software/xorriso/man_1_xorrisofs.html
    # http://www.syslinux.org/wiki/index.php?title=Isohybrid
    if os.path.exists('/usr/lib/ISOLINUX/isohdpfx.bin'):
        # Ubuntu 15.04 uses isolinux (/usr/lib/ISOLINUX/isohdpfx.bin).
        logger.log_data(
            'Use xorriso with isohybrid MBR',
            '/usr/lib/ISOLINUX/isohdpfx.bin')

        if os.path.exists(efi_image_filepath):
            command = (
                'xorriso'
                ' -as mkisofs -r -V "%s" -cache-inodes -J -l'
                ' -iso-level 3'
                ' -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin'
                ' -c isolinux/boot.cat'
                ' -b isolinux/isolinux.bin'
                '  -no-emul-boot'
                '  -boot-load-size 4'
                '  -boot-info-table'
                ' -eltorito-alt-boot'
                '  -e boot/grub/efi.img'
                '  -no-emul-boot'
                '  -isohybrid-gpt-basdat'
                ' -o "%s" .' %
                (model.custom_iso_image_volume_id,
                 custom_iso_image_filepath))
        else:
            command = (
                'xorriso'
                ' -as mkisofs -r -V "%s" -cache-inodes -J -l'
                ' -iso-level 3'
                ' -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin'
                ' -c isolinux/boot.cat'
                ' -b isolinux/isolinux.bin'
                '  -no-emul-boot'
                '  -boot-load-size 4'
                '  -boot-info-table'
                ' -o "%s" .' %
                (model.custom_iso_image_volume_id,
                 custom_iso_image_filepath))
    elif os.path.exists('/usr/lib/syslinux/isohdpfx.bin'):
        # Ubuntu 14.04 uses syslinux-common (/usr/lib/syslinux/isohdpfx.bin).
        logger.log_data(
            'Use xorriso with isohybrid MBR',
            '/usr/lib/syslinux/isohdpfx.bin')

        if os.path.exists(efi_image_filepath):
            command = (
                'xorriso'
                ' -as mkisofs -r -V "%s" -cache-inodes -J -l'
                ' -iso-level 3'
                ' -isohybrid-mbr /usr/lib/syslinux/isohdpfx.bin'
                ' -c isolinux/boot.cat'
                ' -b isolinux/isolinux.bin'
                '  -no-emul-boot'
                '  -boot-load-size 4'
                '  -boot-info-table'
                ' -eltorito-alt-boot'
                '  -e boot/grub/efi.img'
                '  -no-emul-boot'
                '  -isohybrid-gpt-basdat'
                ' -o "%s" .' %
                (model.custom_iso_image_volume_id,
                 custom_iso_image_filepath))
        else:
            command = (
                'xorriso'
                ' -as mkisofs -r -V "%s" -cache-inodes -J -l'
                ' -iso-level 3'
                ' -isohybrid-mbr /usr/lib/syslinux/isohdpfx.bin'
                ' -c isolinux/boot.cat'
                ' -b isolinux/isolinux.bin'
                '  -no-emul-boot'
                '  -boot-load-size 4'
                '  -boot-info-table'
                ' -o "%s" .' %
                (model.custom_iso_image_volume_id,
                 custom_iso_image_filepath))
    else:
        logger.log_data('Use mkisofs', 'No isohybrid MBR available.')
        command = (
            'mkisofs -r -V "%s" -cache-inodes -J -l'
            ' -iso-level 3'
            ' -c isolinux/boot.cat'
            ' -b isolinux/isolinux.bin'
            '  -no-emul-boot'
            '  -boot-load-size 4'
            '  -boot-info-table'
            ' -o "%s" .' %
            (model.custom_iso_image_volume_id,
             custom_iso_image_filepath))

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)

    execute_asynchronous(command, thread, custom_live_iso_directory)
    logger.log_data('• The start time is', formatted_time)

    progress_initial = 0
    progress_target = 100
    progress_display = progress_initial - 1
    progress_current = progress_initial

    while (thread.process.exitstatus is
           None) or (progress_display < progress_target
                     and not thread.process.exitstatus):

        try:
            line = thread.process.read_nonblocking(100, 0.05)
            logger.log_data('• Status', line)
            result = re.search(r'([0-9]{1,3})%', str(line))
            if result:
                progress_current = progress_initial + int(result.group(1))
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            if progress_current < progress_target:
                progress_current = progress_target
            time.sleep(0.05)

        if progress_current > progress_display:
            progress_display += 1
            if progress_display % 10 == 0:
                logger.log_data('• Completed', '%i%%' % progress_display)
            if progress_display == 0:
                display.update_progressbar_text(
                    'repackage_iso_page__create_iso_image_progressbar',
                    None)
            display.update_progressbar_percent(
                'repackage_iso_page__create_iso_image_progressbar',
                progress_display)

    current_time = datetime.datetime.now()
    # formatted_time = '{:%Y-%m-%d %I:%M:%S.%f %p}'.format(current_time)
    formatted_time = '{:%H:%M:%S.%f}'.format(current_time)
    logger.log_data('• The end time is', formatted_time)

    os.chown(custom_iso_image_filepath, model.user_id, model.group_id)

    time.sleep(0.10)


def calculate_md5_hash_for_iso():
    logger.log_note('Calculate md5 sum')

    custom_iso_image_filepath = os.path.realpath(
        model.custom_iso_image_filepath)
    md5_sum = calculate_md5_hash_for_file(custom_iso_image_filepath)
    model.set_custom_iso_image_md5_sum(md5_sum)

    custom_iso_image_md5_filepath = os.path.realpath(
        model.custom_iso_image_md5_filepath)

    logger.log_data('Write ISO md5sum to', custom_iso_image_md5_filepath)
    with open(custom_iso_image_md5_filepath, 'w') as md5_sum_file:
        md5_sum_file.write(
            '%s  %s' % (md5_sum,
                        model.custom_iso_image_filename))

    os.chown(
        model.custom_iso_image_md5_filepath,
        model.user_id,
        model.group_id)
