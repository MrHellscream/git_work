import sys
import os


import TabSDF as tabSDF
# from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget
from PyQt5.QtCore import QSize, Qt
import constants

# Ui_MainWindow, QMainWindow = loadUiType('gui\mainwindow.ui')


class Main(QMainWindow):
    def __init__(self, projectFolderPath):
        super(Main, self).__init__()
        # self.setupUi(self)

        self.projectFolderPath_ = projectFolderPath

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

        self.tabs.addTab(self.tab1, "Search for duplicate files")

        self.setCentralWidget(self.tabs)

        # self.tabSDF_ = tabSDF.TabSDFWidget(self, self.projectFolderPath_)

    def update(self):
        self.tab1.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    # only folder.
    projectFolderPath = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())

    if projectFolderPath:
        print('projectFolderPath ' + projectFolderPath)

        main = Main(projectFolderPath)
        main.show()
        main.update()

        print('exit')
        sys.exit(app.exec_())
