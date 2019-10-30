#!/usr/bin/python3

########################################################################
#                                                                      #
# transition.py                                                        #
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
import transitions

import ctypes
import sys
from threading import Thread
import time
import traceback

########################################################################
# InterruptException Class
########################################################################


class InterruptException(Exception):

    pass


########################################################################
# TransitionThread Thread
########################################################################


class TransitionThread(Thread):

    process = None

    def __init__(self, page_name, new_page_name, previous_thread=None):

        if previous_thread:
            logger.log_step('Created new thread')
            logger.log_data('Current page', page_name)
            logger.log_data('New page', new_page_name)
            logger.log_data('Previous thread id', previous_thread.ident)
        else:
            logger.log_step('Created new thread')
            logger.log_data('Current page', page_name)
            logger.log_data('New page', new_page_name)

        # Set instance variables
        self.page_name = page_name
        self.new_page_name = new_page_name
        self.previous_thread = previous_thread
        self.process = None

        Thread.__init__(self)

    def run(self):

        thread_id = self.ident
        logger.log_data('Running thread with id', thread_id)

        self.interrupt_previous_thread()

        # The "action" function invokes the "transition__from..." functions.
        # The "transition__from..." functions should not catch any exceptions.
        # Instead, any exceptions should propogate , w they will be
        # ignored.  The old thread and associated process(es) will be stopped.
        # It is the responsibility of the new canceling thread to clean up after
        # the old canceled thread.
        try:
            self.action()
        except InterruptException as exception:
            logger.log_data(
                'InterruptException encountered in thread',
                self.ident)
            logger.log_data('Ignore exception?', 'Yes')
            # logger.log_data('The exception is', exception)
            # logger.log_data('The tracekback is', traceback.format_exc())
        except Exception as exception:
            logger.log_data('Exception encountered in thread', self.ident)
            logger.log_data('Ignore exception?', 'No')
            # logger.log_data('The exception is', exception)
            logger.log_data('The tracekback is', traceback.format_exc())

        logger.log_data('Finished running thread with id', thread_id)

    def get_process_id(self):

        if self.process:
            return self.process.pid
        else:
            return -1

    def get_process(self):

        if self.process:
            logger.log_data(
                'Get process',
                'Returning process with id %i.' % self.process.pid)
            return self.process
        else:
            logger.log_data(
                'Get process',
                'Process does not exists, return None.')
            return None

    def set_process(self, new_process):

        self.process = new_process
        # logger.log_data('Set the new process for thread with id %s ' % self.ident, 'The new process id is %s' % self.process.pid)
        logger.log_data('Set a new process for thread id', self.ident)
        logger.log_data('The new process id is', self.process.pid)

    def interrupt_previous_thread(self):

        # logger.log_note('Interrupt previous thread')
        sys.stdout.flush()
        if self.previous_thread and self.previous_thread.is_alive():

            display.show_spinner()
            display.reset_buttons()
            time.sleep(0.125)

            if self.previous_thread and self.previous_thread.is_alive():

                previous_thread_id = self.previous_thread.ident
                logger.log_data(
                    'Interrupting previous thread with id',
                    previous_thread_id)
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(previous_thread_id),
                    ctypes.py_object(InterruptException))
                self.terminate_process(self.previous_thread)
                self.previous_thread.join()
                # time.sleep(0.50)
                logger.log_data(
                    'Done interrupting previous thread with id',
                    previous_thread_id)

            display.hide_spinner()

        else:

            logger.log_data(
                'Interrupting previous thread with id',
                'No previous thread to interrupt')

    def terminate_process(self, previous_thread):
        # TODO: Handle errors
        #       - Raise ExceptionPexpect('Could not terminate the child.')
        #       - Cannot wait for dead child process

        process = previous_thread.process

        if process:

            logger.log_data('Is there a process running?', True)

            process_id = previous_thread.get_process_id()
            logger.log_data('Terminating process with id', process_id)

            is_alive = process.isalive()
            logger.log_data(
                'Is process with id %s alive?' % process_id,
                is_alive)

            is_terminated = False
            if is_alive:
                try:
                    logger.log_data(
                        'Trying to terminate process with id',
                        process_id)
                    is_terminated = process.terminate(True)
                except Exception as exception:
                    logger.log_data(
                        'Exception encountered in thread',
                        self.ident)
                    logger.log_data(
                        'Exception encountered terminating process with id',
                        process_id)
                    # logger.log_data('The exception is', exception)
                    logger.log_data(
                        'The tracekback is',
                        traceback.format_exc())
                    try:
                        logger.log_data(
                            'Trying to wait for process with id',
                            process_id)
                        # If the process is no longer alive, consider it terminated.
                        process.wait()
                        is_terminated = not process.isalive()
                    except Exception as exception:
                        logger.log_data(
                            'Exception encountered in thread',
                            self.ident)
                        logger.log_data(
                            'Exception encountered waiting for process with id',
                            process_id)
                        # logger.log_data('The exception is', exception)
                        logger.log_data(
                            'The tracekback is',
                            traceback.format_exc())
                    else:
                        logger.log_data(
                            'Finished trying to wait for process with id',
                            process_id)
                else:
                    logger.log_data(
                        'Finished trying to terminate process with id',
                        process_id)
            else:
                is_terminated = True

            logger.log_data(
                'Process %s terminated?' % process_id,
                is_terminated)

        else:
            logger.log_data('Is there a process running?', False)

    def action(self):

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

        logger.log_step('Performing requested transition action')
        logger.log_data('Transition from', self.page_name)
        logger.log_data('Transition to', self.new_page_name)

        # TODO: After making the to 'TODO' changes below, move this section after the "elif self.page_name == 'project_directory_page'" section below.
        if self.page_name == 'project_directory_page__project_directory_filechooser':
            if self.new_page_name == 'project_directory_page':
                transitions.transition__from__project_directory_page__project_directory_filechooser__to__project_directory_page(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'original_iso_image_filepath_filechooser':
            # TODO: Notice the page name below is 'original_iso_image_filepath_filechooser'.
            #       For consistency, consider using separate transitions for
            #       - new_project_page_original_iso_image_filepath_filechooser
            #       - existing_project_page_original_iso_image_filepath_filechooser
            #       Place new code after "New Project" and after "Existing Project Page" sections below.
            if self.new_page_name == 'new_project_page':
                transitions.transition__from__original_iso_image_filepath_filechooser__to__new_project_page(
                    self)
            elif self.new_page_name == 'existing_project_page':
                transitions.transition__from__original_iso_image_filepath_filechooser__to__existing_project_page(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'custom_iso_image_directory_filechooser':
            # TODO: Notice the page name below is 'custom_iso_image_directory_filechooser'.
            #       For consistency, consider using separate transitions for
            #       - new_project_page_custom_iso_image_directory_filechooser
            #       - existing_project_page_custom_iso_image_directory_filechooser
            #       Place new code after "New Project" and after "Existing Project Page" sections below.
            if self.new_page_name == 'new_project_page':
                transitions.transition__from__custom_iso_image_directory_filechooser__to__new_project_page(
                    self)
            elif self.new_page_name == 'existing_project_page':
                transitions.transition__from__custom_iso_image_directory_filechooser__to__existing_project_page(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'project_directory_page':
            if self.new_page_name == 'new_project_page':
                # New Project
                transitions.transition__from__project_directory_page__to__new_project_page(
                    self)
            elif self.new_page_name == 'existing_project_page':
                # Existing Project
                transitions.transition__from__project_directory_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__project_directory_page__to__exit(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'new_project_page':
            # TODO: Add a transition to
            #       - new_project_page_original_iso_image_filepath_filechooser
            #       - new_project_page_custom_iso_image_directory_filechooser
            #       Instead of using
            #       - handlers.on_clicked__new_project_page__original_iso_image_filepath_filechooser__open_button()
            #       - handlers.on_clicked__new_project_page__custom_iso_image_directory_filechooser__open_button()
            if self.new_page_name == 'terminal_page':
                transitions.transition__from__new_project_page__to__terminal_page(
                    self)
            elif self.new_page_name == 'project_directory_page':
                transitions.transition__from__new_project_page__to__project_directory_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__new_project_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'existing_project_page':
            # TODO: Add a transition to...
            #       - existing_project_page_original_iso_image_filepath_filechooser
            #       - existing_project_page_custom_iso_image_directory_filechooser
            #       Instead of using...
            #       - handlers.on_clicked__existing_project_page__original_iso_image_filepath_filechooser__open_button()
            #       - handlers.on_clicked__existing_project_page__custom_iso_image_directory_filechooser__open_button()
            if self.new_page_name == 'existing_project_page':
                transitions.transition__from__existing_project_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'options_page':
                transitions.transition__from__existing_project_page__to__options_page(
                    self)
            elif self.new_page_name == 'terminal_page':
                transitions.transition__from__existing_project_page__to__terminal_page(
                    self)
            elif self.new_page_name == 'delete_project_page':
                transitions.transition__from__existing_project_page__to__delete_project_page(
                    self)
            elif self.new_page_name == 'project_directory_page':
                transitions.transition__from__existing_project_page__to__project_directory_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__existing_project_page__to__exit(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'delete_project_page':
            if self.new_page_name == 'new_project_page':
                transitions.transition__from__delete_project_page__to__new_project_page(
                    self)
            elif self.new_page_name == 'existing_project_page':
                transitions.transition__from__delete_project_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__delete_project_page__to__exit(
                    self)
        elif self.page_name == 'unsquashfs_page':
            # TODO: This transition is automatic, so this section is not used.
            # if self.new_page_name == 'terminal_page':
            #    transitions.transition__from__unsquashfs_page__to__terminal_page(self)
            if self.new_page_name == 'existing_project_page':
                transitions.transition__from__unsquashfs_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__unsquashfs_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'terminal_page':
            if self.new_page_name == 'options_page':
                transitions.transition__from__terminal_page__to__options_page(
                    self)
            elif self.new_page_name == 'copy_files_page':
                transitions.transition__from__terminal_page__to__copy_files_page(
                    self)
            elif self.new_page_name == 'existing_project_page':
                transitions.transition__from__terminal_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'terminal_page':
                transitions.transition__from__terminal_page__to__terminal_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__terminal_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'copy_files_page':
            if self.new_page_name == 'terminal_page_copy_files':
                # TODO: Consider converting to (page, function) instead of (page, page)
                transitions.transition__from__copy_files_page__to__terminal_page_copy_files(
                    self)
            elif self.new_page_name == 'terminal_page_cancel_copy_files':
                transitions.transition__from__copy_files_page__to__terminal_page_cancel_copy_files(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__copy_files_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'options_page':
            if self.new_page_name == 'existing_project_page':
                transitions.transition__from__options_page__to__existing_project_page(
                    self)
            elif self.new_page_name == 'repackage_iso_page':
                transitions.transition__from__options_page__to__repackage_iso_page(
                    self)
            elif self.new_page_name == 'terminal_page':
                transitions.transition__from__options_page__to__terminal_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__options_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'repackage_iso_page':
            if self.new_page_name == 'finish_page':
                transitions.transition__from__repackage_iso_page__to__finish_page(
                    self)
            elif self.new_page_name == 'options_page':
                transitions.transition__from__repackage_iso_page__to__options_page(
                    self)
            elif self.new_page_name == 'exit':
                transitions.transition__from__repackage_iso_page__to__exit(
                    self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        elif self.page_name == 'finish_page':
            if self.new_page_name == 'exit':
                transitions.transition__from__finish_page__to__exit(self)
            else:
                # Error
                logger.log_data(
                    'Error. No action defined for transition to',
                    self.new_page_name)
        else:
            # Error
            logger.log_data(
                'Error. No action defined for transition',
                'From %s to %s' % (self.page_name,
                                   self.new_page_name))
