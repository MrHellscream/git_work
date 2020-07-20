import sys
import os

# from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget
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
        self.width = 800
        self.height = 600

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


    def update(self):
        self.tab1.update()

    def onChangeTab(self, index):
        print('sssss', index)
        self.tabs.currentWidget().update()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # only folder.
    projectFolderPath = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())

    if projectFolderPath:
        main = Main(projectFolderPath)
        main.show()
        main.update()

        sys.exit(app.exec_())
