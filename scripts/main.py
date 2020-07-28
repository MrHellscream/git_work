import sys
import os

import constants as const
import configHelpers as confHelper
# from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget, QAction
from PyQt5.QtCore import QSize

import logging

import TabSDF as tabSDF
import TabSDS as tabSDS
import constants

# Ui_MainWindow, QMainWindow = loadUiType('gui\mainwindow.ui')



class Main(QMainWindow):
    def __init__(self, folder_path):
        super(Main, self).__init__()
        # self.setupUi(self)

        self.project_folder_path_ = folder_path

        self.title = self.project_folder_path_
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 600

        # TABS

        self.setWindowTitle(self.title)
        self.setFixedSize(QSize(self.width, self.height))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabs = QTabWidget()

        self.tab1 = tabSDF.TabSDFWidget(self)
        self.tab2 = tabSDS.TabSDSWidget(self)

        self.tabs.addTab(self.tab1, "Search unused layers")
        self.tabs.addTab(self.tab2, "Search unused sounds")

        self.tabs.currentChanged.connect(self.onChangeTab)

        self.setCentralWidget(self.tabs)


        # MENU

        extractAction = QAction("&New Project", self)
        # extractAction.setShortcut("Ctrl+O")
        # extractAction.setStatusTip('New Project')
        extractAction.triggered.connect(self.newProject)

        # self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)


    def getProjectFolderPath(self):
        return self.project_folder_path_

    def setProjectFolderPath(self, folder_path):
        self.project_folder_path_ = folder_path

    def updateTitle(self):
        print('new_project_folder_path ' + self.project_folder_path_)
        self.title = self.getProjectFolderPath()
        self.setWindowTitle(self.title)

    def update(self):
        self.tab1.update(self.getProjectFolderPath())

    def onChangeTab(self, index):
        print('sssss', index)
        self.tabs.currentWidget().update(self.getProjectFolderPath())


    def newProject(self):
        new_project_folder_path = QFileDialog.getExistingDirectory(None,
                                                                   'Select project folder:',
                                                                   self.project_folder_path_)

        if new_project_folder_path and os.path.exists(new_project_folder_path):
            print(new_project_folder_path)
            confHelper.saveProjectFolderPathToConfig(const.CONFIG_PATH, new_project_folder_path)


            self.setProjectFolderPath(new_project_folder_path)

            self.updateTitle()

            self.tabs.currentWidget().update(self.getProjectFolderPath())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    project_folder_path = None



    if os.path.exists(const.CONFIG_PATH):
        project_folder_path = confHelper.getProjectFolderPathFromConfig(const.CONFIG_PATH)

    else:
        confHelper.createConfig(const.CONFIG_PATH)



    if not project_folder_path:
        # only folder.
        project_folder_path = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())

        confHelper.saveProjectFolderPathToConfig(const.CONFIG_PATH, project_folder_path)




    if project_folder_path:
        main = Main(project_folder_path)
        main.show()
        main.update()

        sys.exit(app.exec_())
