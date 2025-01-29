import sys
import os

from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget, QAction
from PyQt5.QtCore import QSize

from .Tab import TabSDFWidget, TabSDSWidget, TabSDTWidget, TabSUIWidget

import constants as const
import configHelpers as confHelper


class Main(QMainWindow):
    def __init__(self, folder_path):
        QMainWindow.__init__(self)
        # self.setupUi(self)

        self.project_folder_path_ = folder_path

        self.title = self.project_folder_path_


        # TABS
        window_size = const.WINDOW_SIZE

        self.setWindowTitle(self.title)
        self.setFixedSize(QSize(window_size['width'], window_size['height']))
        self.setGeometry(window_size['left'], window_size['top'],  window_size['width'], window_size['height'])

        self.tabs = QTabWidget()

        self.tab1 = TabSDFWidget(self)
        self.tab2 = TabSDSWidget(self)
        self.tab3 = TabSDTWidget(self)
        self.tab4 = TabSUIWidget(self)

        self.tabs.addTab(self.tab1, "Search unused layers")
        self.tabs.addTab(self.tab2, "Search unused sounds")
        self.tabs.addTab(self.tab3, "Search duplicate values in texts")
        self.tabs.addTab(self.tab4, "Search unused items")

        self.tabs.currentChanged.connect(self.onChangeTab)

        self.setCentralWidget(self.tabs)


        # MENU
        extract_action = QAction("&New Project", self)
        # extract_action.setShortcut("Ctrl+O")
        # extract_action.setStatusTip('New Project')
        extract_action.triggered.connect(self.newProject)

        # self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(extract_action)


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
        print('onChangeTab', index)
        self.tabs.currentWidget().update(self.getProjectFolderPath())


    def newProject(self):
        new_project_folder_path = QFileDialog.getExistingDirectory(None,
                                                                   'Select project folder:',
                                                                   self.project_folder_path_)

        if new_project_folder_path and os.path.exists(new_project_folder_path):
            print(new_project_folder_path)
            confHelper.save_project_folder_path_to_config(const.CONFIG_PATH, new_project_folder_path)

            self.setProjectFolderPath(new_project_folder_path)

            self.updateTitle()

            self.tabs.currentWidget().update(self.getProjectFolderPath())


def StartApp():
    app = QApplication(sys.argv)

    project_folder_path = None

    if os.path.exists(const.CONFIG_PATH):
        project_folder_path = confHelper.get_project_folder_path_from_config(const.CONFIG_PATH)
    else:
        confHelper.create_config(const.CONFIG_PATH)

    if not project_folder_path:

        # only folder.
        project_folder_path = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())

        confHelper.save_project_folder_path_to_config(const.CONFIG_PATH, project_folder_path)


    if project_folder_path:
        main = Main(project_folder_path)
        main.show()
        main.update()

        sys.exit(app.exec_())
    # return app
