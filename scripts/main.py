import sys
import os
import json
import constants as const

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
    def __init__(self, project_folder_path):
        super(Main, self).__init__()
        # self.setupUi(self)

        self.projectFolderPath_ = project_folder_path

        self.title = 'Test'
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 600

        # TABS

        self.setWindowTitle(self.title)
        self.setFixedSize(QSize(self.width, self.height))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabs = QTabWidget()

        self.tab1 = tabSDF.TabSDFWidget(self, self.projectFolderPath_)
        self.tab2 = tabSDS.TabSDSWidget(self, self.projectFolderPath_)

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


    def update(self):
        self.tab1.update()

    def onChangeTab(self, index):
        print('sssss', index)
        self.tabs.currentWidget().update()

    def newProject(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    project_folder_path = None



    config_data = {}

    if os.path.exists(const.CONFIG_PATH):
        try:
            with open(const.CONFIG_PATH) as config_file:
                config_data = json.load(config_file)
        except json.JSONDecodeError:
            print('Upsss ' + const.CONFIG_PATH + ' is empty')

        project_folder_path = config_data.get('projectFolderPath')

        print(config_data)

    else:
        config_file = open(const.CONFIG_PATH, "w")
        config_data = {'projectFolderPath': None}

        json.dump(config_data, config_file)

        config_file.close()


    if not project_folder_path or not os.path.exists(project_folder_path):
        # only folder.
        project_folder_path = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())

        config_data = {'projectFolderPath': project_folder_path}
        with open(const.CONFIG_PATH, 'w') as config_file:
            json.dump(config_data, config_file)




    if project_folder_path:
        main = Main(project_folder_path)
        main.show()
        main.update()

        sys.exit(app.exec_())
