#!/usr/bin/python3

########################################################################
#                                                            
# timbrel.py                                          
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
me='timbrel.py'

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
# gi.require_version('GtkSource', '3.0')

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GtkSource
import pwd
import os
import sys
import traceback


import timbrel_cfg
import timbrel_log
import timbrel_handlers

import display
import model
import utilities

try:
    gi.require_version('GtkSource', '4')
    timbrel_log.info(me,'Using GtkSource version', '4')
except ValueError:
    gi.require_version('GtkSource', '3.0')
    timbrel_log.info(me,'Using GtkSource version', '3.0')


def cubic_versionGet():
	strVersion = "incorrectVersion"
	try:
		f = open(timbrel_cfg.path + "/version.txt", "r")
		strVersion = f.read(5)
	except FileNotFoundError:
		pass
	return strVersion

try:
    timbrel_log.info(me,'Starting Timbrel')

    user_id = os.getuid()
    if user_id != 0:
        timbrel_log.error(me,'This program requires root access. Please run as "sudo -H '+__file__+'".')
        sys.exit(1)
    model.set_root_user_id(user_id)
    root_gid = os.getgid()
    model.set_root_group_id(root_gid)

# working directory
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            working_directory = sys.argv[1]
        else:
            timbrel_log.info(me,'Directory '+sys.argv[1]+' does not exist. Usigng script location as working directory.')
            working_directory = timbrel_cfg.path
    else:
        working_directory = timbrel_cfg.path

    os.chdir(working_directory)
    current_directory = os.getcwd()
    timbrel_log.info(me,'The working directory is', current_directory)

    uid = int(os.getuid() )
    pw_name, pw_passwd, pw_uid, pw_gid, pw_gecos, pw_dir, pw_shell = pwd.getpwuid(
        uid)

    model.set_user_name(pw_name)
    model.set_user_id(pw_uid)
    model.set_group_id(pw_gid)
    model.set_home(os.path.expanduser(pw_dir))
    os.environ['HOME'] = model.home
    timbrel_log.info(me,'Set the HOME environment variable to', model.home)



    gtk_version = utilities.get_package_version('gir1.2-gtk-3.0')[0:4]
    timbrel_log.info(me,'The GTK version is', gtk_version)
    if float(gtk_version) < 3.18:
        timbrel_ui_filename = timbrel_cfg.path + '/ui/timbrel_gtk310.ui'
        filechoosers_ui_filename = timbrel_cfg.path + '/ui/filechoosers_gtk310.ui'
    else:
        timbrel_ui_filename = timbrel_cfg.path + '/ui/timbrel_gtk318.ui'
        filechoosers_ui_filename = timbrel_cfg.path + '/ui/filechoosers_gtk318.ui'

    timbrel_log.info(me,'The Timbrel user interface filename is', timbrel_ui_filename)
    timbrel_log.info(me,
        'The filechoosers user interface filename is',
        timbrel_ui_filename)

    GObject.type_register(GtkSource.View)
    builder = Gtk.Builder.new_from_file(timbrel_ui_filename)
    builder.add_from_file(filechoosers_ui_filename)

    model.set_builder(builder)

    # TODO: Workaround for error:
    # (cubic.py:2790): dconf-CRITICAL **: 09:34:53.072: unable to create file
    # '/home/<user>/.cache/dconf/user': Permission denied. dconf will not work
    # properly.
    dconf_directory = os.path.join(model.home, '.cache', 'dconf')
    try:
        os.chown(dconf_directory, model.user_id, model.group_id)
    except FileNotFoundError:
        pass

    builder.connect_signals(timbrel_handlers)

    model.set_page_name('project_directory_page')
    
    cubic_version = cubic_versionGet()
    model.set_cubic_version(cubic_version)

    window = builder.get_object('window')

    css_provider = Gtk.CssProvider()

    css_provider.load_from_path(timbrel_cfg.path + '/css/cubic.css')

    screen = Gdk.Screen.get_default()
    style_context = window.get_style_context()
    style_context.add_provider_for_screen(
        screen,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# gtk theme and icons
    icon_theme = Gtk.IconTheme.get_default()
    theme_name = Gtk.Settings.get_default().get_property('gtk-theme-name')
    timbrel_log.info(me,'The current GTK theme is', theme_name)

    
    icon_theme_name = Gtk.Settings.get_default().get_property('gtk-icon-theme-name')
    timbrel_log.info(me,'Initial GTK icon_theme is', icon_theme_name)   
    Gtk.Settings.get_default().set_property("gtk-icon-theme-name", "Timbrel")
    icon_theme_name = Gtk.Settings.get_default().get_property('gtk-icon-theme-name')
    timbrel_log.info(me,'The current GTK icon_theme is', icon_theme_name) 

    icon_theme_search_path = icon_theme.get_search_path()
    timbrel_log.info(me,'Replace GTK icon_theme_search_path from ... ',icon_theme_search_path)     
    icon_theme_search_path = [timbrel_cfg.path + '/icons/gtk+-3.18.9' , timbrel_cfg.path + '/icons' ]     
    Gtk.IconTheme.set_search_path(icon_theme,icon_theme_search_path)
    timbrel_log.info(me,'... to', icon_theme_search_path)  

    theme_style = display.get_theme_style(window)
    
#start gtk
    window.show()
    Gtk.main()

except IndexError as exception:
    timbrel_log.error(me,'The tracekback is', traceback.format_exc())
except TypeError as exception:
    timbrel_log.error(me,'The tracekback is', traceback.format_exc())
except Exception as exception:
    timbrel_log.error(me,'The tracekback is', traceback.format_exc())
