import os
import search_duplicate_files as sdf
import constants as const
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel

class TabSDFWidget(QWidget):
    def __init__(self, parent, projectFolderPath):
        super(QWidget, self).__init__(parent)
        # self.window_ = window
        self.projectFolderPath_ = projectFolderPath

        self.horizontLayout = QHBoxLayout(self)

        self.scenesListWidget = QListWidget()
        self.filesListWidget = QListWidget()

        self.sceneListLabel = QLabel('Scenes')
        self.filesListLabel = QLabel('Files')

        self.sceneLayout = QVBoxLayout(self)
        self.filesLayout = QVBoxLayout(self)

        self.sceneLayout.addWidget(self.sceneListLabel)
        self.filesLayout.addWidget(self.filesListLabel)

        self.sceneLayout.addWidget(self.scenesListWidget)
        self.filesLayout.addWidget(self.filesListWidget)



        self.horizontLayout.addLayout(self.sceneLayout)
        self.horizontLayout.addLayout(self.filesLayout)





        self.verticalLayout = QVBoxLayout(self)

        self.openFileButton = QPushButton("OpenFile")
        self.openFolderButton = QPushButton("OpenFolder")
        self.deleteFileButton = QPushButton("DeleteFile")

        self.verticalLayout.addWidget(self.openFileButton)
        self.verticalLayout.addWidget(self.openFolderButton)
        self.verticalLayout.addWidget(self.deleteFileButton)

        self.horizontLayout.addLayout(self.verticalLayout)
        self.setLayout(self.horizontLayout)

        self.scenesListWidget.itemSelectionChanged.connect(self.__tab1_scene_selection_changed)
        self.filesListWidget.itemSelectionChanged.connect(self.__tab1_file_selection_changed)


        self.openFileButton.clicked.connect(self.__openFileButtonClick)
        self.openFolderButton.clicked.connect(self.__openFolderButtonClick)
        self.deleteFileButton.clicked.connect(self.__deleteFileButtonClick)

        self.setTabButtonsEnabled(False)


    def setTabButtonsEnabled(self, enable):
        self.openFileButton.setEnabled(enable)
        self.openFolderButton.setEnabled(enable)
        self.deleteFileButton.setEnabled(enable)


    def update(self):
        path_to_scenes_texture = self.projectFolderPath_ + const.PREFIX_PATH_TO_SCENES_TEXTURE
        if not os.path.exists(path_to_scenes_texture):
            print('What went wrong!!!!Maybe can not open folder: ' + path_to_scenes_texture)
            return


        for file_name in os.listdir(path_to_scenes_texture):
            path = os.path.join(self.projectFolderPath_, file_name)
            if not os.path.isfile(path):
                self.scenesListWidget.addItem(file_name)




    def __tab1_scene_selection_changed(self):
        current_item = self.scenesListWidget.currentItem().text()
        print('__tab1_scene_selection_changed ' + current_item)

        path_to_scenes_texture = self.projectFolderPath_ + const.PREFIX_PATH_TO_SCENES_TEXTURE + current_item
        path_to_scenes_scripts = self.projectFolderPath_ + const.PREFIX_PATH_TO_SCENES_SCRIPTS + current_item

        files_texture = sdf.merge(sdf.walk_texture(path_to_scenes_texture))
        files_scripts = sdf.walk_scripts(path_to_scenes_scripts)

        files_texture_unused = sdf.walk(path_to_scenes_scripts, files_scripts, files_texture)
        # print(files_texture_unused)

        self.filesListWidget.clear()
        self.setTabButtonsEnabled(False)
        for abs_name in files_texture_unused:
            if os.path.isfile(abs_name):
                self.filesListWidget.addItem(abs_name.replace('\\', '/'))


    def __tab1_file_selection_changed(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            self.setTabButtonsEnabled(True)
        else:
            self.setTabButtonsEnabled(False)


    def __openFileButtonClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            path_to_file = current_item.text()
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)


    def __openFolderButtonClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            path_to_file = current_item.text()
            path_to_folder = os.path.split(path_to_file)[0]

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))


    def __deleteFileButtonClick(self):
        current_item = self.filesListWidget.currentItem()

        if current_item:
            path_to_file = current_item.text()
            if os.path.exists(path_to_file):
                try:
                    os.remove(path_to_file)
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))
                    return
            else:
                print("The file does not exist")

            selected_items = self.filesListWidget.selectedItems()
            for item in selected_items:
                self.filesListWidget.takeItem(self.filesListWidget.row(item))
        else:
            return