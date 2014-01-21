#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OSGeo4Mac Python startup script for setting CMake option string for use in
 Qt Creator with dev builds and installs of QGIS when built off dependencies
 from homebrew-osgeo4mac tap
                              -------------------
        begin    : January 2014
        copyright: (C) 2014 Larry Shaffer
        email    : larrys at dakotacarto dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from collections import OrderedDict

HOME = os.path.expanduser('~')
SRC_DIR = HOME + '/QGIS/github.com/QGIS'
INSTALL_PREFIX = HOME + '/QGIS/github.com/QGIS_Apps_osgeo4mac'

HOMEBREW_PREFIX = '/usr/local'
if 'HOMEBREW_PREFIX' in os.environ:
    HOMEBREW_PREFIX = os.environ['HOMEBREW_PREFIX']

GRASS_VERSION = '6.4.3'
OSG_VERSION = '3.2.0'

# ensure libintl.h can be found in gettext for grass
CXX_FLGS = "-I{hb}/opt/gettext/include"
if 'CXXFLAGS' in os.environ:
    CXX_FLGS += " " + os.environ['CXXFLAGS']

# search Homebrew's Frameworks directory before those in /Library or /System
LD_FLGS = "-F{hb}/Frameworks"
if 'LDFLAGS' in os.environ:
    LD_FLGS += " " + os.environ['LDFLAGS']

# IMPORTANT: mulit-path options need the CMake list semicolon (;) delimiter,
#            NOT the environment variable path list colon (:) separator

# set CMAKE_PREFIX_PATH for keg-only installs, and HOMEBREW_PREFIX

opts = OrderedDict([
    ('CMAKE_INSTALL_PREFIX', INSTALL_PREFIX),
    ('CMAKE_PREFIX_PATH', '"{hb}/opt/libxml2;{hb}/opt/expat;{hb}/opt/gettext;{hb}/opt/sqlite;{hb}"'),
    ('CMAKE_BUILD_TYPE', 'RelWithDebInfo'),
    ('CMAKE_FIND_FRAMEWORK', 'LAST'),
    ('CMAKE_CXX_FLAGS', '"' + CXX_FLGS + '"'),
    ('CMAKE_EXE_LINKER_FLAGS', '"' + LD_FLGS + '"'),
    ('CMAKE_MODULE_LINKER_FLAGS', '"' + LD_FLGS + '"'),
    ('CMAKE_SHARED_LINKER_FLAGS', '"' + LD_FLGS + '"'),
    ('CXX_EXTRA_FLAGS', '"-isystem-prefix {hb} -Wno-unused-private-field"'),
    ('BISON_EXECUTABLE', '{hb}/opt/bison/bin/bison'),
    ('QT_QMAKE_EXECUTABLE', '{hb}/bin/qmake'),
    ('GITCOMMAND', '{hb}/bin/git'),
    ('ENABLE_TESTS', 'TRUE'),
    ('WITH_ASTYLE', 'TRUE'),
    ('WITH_INTERNAL_SPATIALITE', 'FALSE'),
    ('WITH_PYSPATIALITE', 'FALSE'),
    ('QWT_LIBRARY', '{hb}/opt/qwt/lib/qwt.framework/qwt'),
    ('QWT_INCLUDE_DIR', '{hb}/opt/qwt/lib/qwt.framework/Headers'),
    ('WITH_INTERNAL_QWTPOLAR', 'FALSE'),
    ('WITH_MAPSERVER', 'TRUE'),
    ('WITH_STAGED_PLUGINS', 'FALSE'),
    ('WITH_PY_COMPILE', 'TRUE'),
    ('WITH_APIDOC', 'FALSE'),
    ('WITH_QSCIAPI', 'FALSE'),
    ('POSTGRES_CONFIG', '{hb}/bin/pg_config'),
    ('WITH_GRASS', 'TRUE'),
    ('GRASS_PREFIX', '{hb}/opt/grass/grass-{grsv}'),
    ('WITH_GLOBE', 'TRUE'),
    ('OSG_DIR', '{hb}'),
    ('OSGEARTH_DIR', '{hb}'),
    ('OSG_PLUGINS_PATH', '{hb}/lib/osgPlugins-{osgv}'),
    ('QGIS_MACAPP_BUNDLE', '0')
])

# These should be found automatically now...
#     ('SQLITE3_INCLUDE_DIR', '{hb}/opt/sqlite/include'),
#     ('SQLITE3_LIBRARY', '{hb}/opt/sqlite/lib/libsqlite3.dylib'),
#     ('QSCINTILLA_INCLUDE_DIR', '{hb}/opt/qscintilla2/include/Qsci'),
#     ('QSCINTILLA_LIBRARY', '{hb}/opt/qscintilla2/lib/libqscintilla2.dylib'),


if os.path.exists(HOMEBREW_PREFIX + '/Frameworks/Python.framework'):
    opts['PYTHON_EXECUTABLE'] = '{hb}/bin/python'
    opts['PYTHON_CUSTOM_FRAMEWORK'] = '{hb}/Frameworks/Python.framework'

opts_s = SRC_DIR
for k, v in opts.iteritems():
    opts_s += ' -D{0}={1}'.format(k, v.format(hb=HOMEBREW_PREFIX,
                                              grsv=GRASS_VERSION,
                                              osgv=OSG_VERSION))

os.system("echo '{0}' | pbcopy".format(opts_s))
print "The following has been copied to the clipboard:\n"
print opts_s
