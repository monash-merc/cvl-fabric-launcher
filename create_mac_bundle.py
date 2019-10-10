# MASSIVE/CVL Launcher - easy secure login for the MASSIVE Desktop and the CVL
#
# Copyright (c) 2012-2013, Monash e-Research Centre (Monash University, Australia)
# All rights reserved.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# In addition, redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# -  Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# -  Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# -  Neither the name of the Monash University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. SEE THE
# GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#  Enquiries: help@massive.org.au

"""
A distutils script to make a standalone .app of the MASSIVE Launcher for
Mac OS X.  You can get py2app from http://undefined.org/python/py2app.
Use this command to build the .app and collect the other needed files:

   python create_mac_bundle.py py2app

Traditionally, this script would be named setup.py
"""

from setuptools import setup, Extension
import launcher_version_number
import create_commit_def
import requests
import os
import pkgutil
myname="Strudel"

resource_files=["MASSIVE.icns", requests.certs.where(), "masterList.url","/Library/Python/2.7/site-packages/boto/endpoints.json"]

launcherVersionNumberModulePath = os.path.dirname(pkgutil.get_loader("launcher_version_number").filename)
helpFilesDirectory = os.path.join(launcherVersionNumberModulePath, "help", "helpfiles")

for helpFile in os.listdir(helpFilesDirectory):
    helpFilePath = os.path.join(helpFilesDirectory, helpFile)
    if os.path.isfile(helpFilePath): # skip directories
        resource_file = ('help/helpfiles', [helpFilePath])
        resource_files.append(resource_file)

helpDirectory = os.path.join(launcherVersionNumberModulePath, "help")
resource_file = ('help', [os.path.join(helpDirectory, "README.txt")])
resource_files.append(resource_file)

setup(
    options=dict(py2app=dict(
        arch='x86_64',
        plist=dict(
            CFBundleDevelopmentRegion="English",
            CFBundleDisplayName=myname,
            CFBundleExecutable=myname,
            CFBundleIconFile="MASSIVE.icns",
            CFBundleIdentifier="au.edu.monash.MASSIVE",
            CFBundleName="Strudel",
            CFBundlePackageType="APPL",
            CFBundleVersion="Version " + launcher_version_number.version_number,
            LSArchitecturePriority=["x86_64"]
            )
        )
    ),
    data_files=resource_files,
    name=myname,
    setup_requires=["py2app"],
    app=['launcher.py']
)
