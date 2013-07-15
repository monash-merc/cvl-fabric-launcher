#HelpController.py

import sys
import os
import wx.html
import tempfile
import requests
import traceback
import pkgutil
from utilityFunctions import logger_debug, unzip

launcherHtmlHelpProjectFilename = "launcher.hhp"

class HelpController():

    def __init__(self):

        self.wxHtmlHelpController = wx.html.HtmlHelpController(style=wx.html.HF_DEFAULT_STYLE, parentWindow=None)

        self.helpZipFile = None
        self.helpZipFilePath = None
        self.helpZipFileDirectory = None
        self.helpFilesDirectory = None

        #self.launcherHelpUrl = "https://cvl.massive.org.au/launcher_files/help/helpfiles.zip"
        self.launcherHelpUrl = "https://raw.github.com/CVL-dev/cvl-fabric-launcher/master/help/helpfiles.zip"
        self.initializationSucceeded = False
        try:
            # Download helpfiles.zip:

            self.helpZipFile = tempfile.NamedTemporaryFile(mode='w+b', prefix='helpfiles-', suffix='.zip', delete=False)
            self.helpZipFilePath = self.helpZipFile.name
            logger_debug("self.helpZipFilePath = " + self.helpZipFilePath)
            r = requests.get(self.launcherHelpUrl, verify=False)
            if r.status_code == 200:
                for chunk in r.iter_content():
                    self.helpZipFile.write(chunk)
            self.helpZipFile.close()

            # We should be able to add the zip archive directly to the 
            # help controller, but that didn't seem to work.

            # Unzip helpfiles.zip:

            (self.helpZipFileDirectory, self.helpZipFileFilename) = os.path.split(self.helpZipFilePath)
            unzip(self.helpZipFilePath, self.helpZipFileDirectory)
            self.helpFilesDirectory = os.path.join(self.helpZipFileDirectory, "helpfiles")
            logger_debug("self.helpFilesDirectory = " + self.helpFilesDirectory)

            self.launcherHtmlHelpProjectFile = os.path.join(self.helpFilesDirectory, launcherHtmlHelpProjectFilename)
            self.initializationSucceeded = self.wxHtmlHelpController.AddBook(self.launcherHtmlHelpProjectFile)

        except:
            logger_debug(traceback.format_exc())

            try:
                # If we don't succeed in downloading help, 
                # we will try using local help files instead.

                if hasattr(sys, 'frozen'):
                    self.helpFilesDirectory = os.path.join(os.path.dirname(sys.executable), "help", "helpfiles")
                else:
                    launcherModulePath = os.path.dirname(pkgutil.get_loader("launcher").filename)
                    self.helpFilesDirectory = os.path.join(launcherModulePath, "help", "helpfiles")

                self.launcherHtmlHelpProjectFile = os.path.join(self.helpFilesDirectory, launcherHtmlHelpProjectFilename)
                self.initializationSucceeded = self.wxHtmlHelpController.AddBook(self.launcherHtmlHelpProjectFile)

            except:
                logger_debug(traceback.format_exc())


    def cleanUp(self):
        if self.helpZipFilePath is not None:
            os.remove(self.helpZipFilePath)
        if self.helpFilesDirectory is not None:
            for helpFile in os.listdir(self.helpFilesDirectory):
                os.remove(os.path.join(self.helpFilesDirectory,helpFile))
            os.remove(self.helpFilesDirectory)

    # At first I tried inheriting from the wx.html.HtmlHelpController class,
    # so that I would get these methods for free, but then AddBook complained
    # that objects of my derived class were not instances of 
    # wx.html.HtmlHelpController

    def DisplayContents(self):
        self.wxHtmlHelpController.DisplayContents()

    def Display(self,chapter):
        self.wxHtmlHelpController.Display(chapter)

helpController = HelpController()

#helpController.DisplayContents()
#helpController.Display("MASSIVE/CVL Launcher")
#helpController.Display("SSH Keys")
