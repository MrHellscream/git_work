import os
import search_unused_files as suf
import constants as const
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel
from PyQt5.QtCore import QSize


class TabSDFWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        # self.window_ = window

        self.project_folder_path_ = None

        self.sceneInfos = {}

        # GUI Tab
        self.horizontLayout = QHBoxLayout(self)

        self.scenesListWidget = QListWidget()
        self.filesListWidget = QListWidget()

        self.sceneListLabel = QLabel('Scenes')
        self.filesListLabel = QLabel('Files')

        self.sceneLayout = QVBoxLayout(self)
        self.filesLayout = QVBoxLayout(self)

        self.sceneLayout.addWidget(self.sceneListLabel, 0)
        self.filesLayout.addWidget(self.filesListLabel, 0)

        self.sceneLayout.addWidget(self.scenesListWidget)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontLayout.addLayout(self.sceneLayout, 15)
        self.horizontLayout.addLayout(self.filesLayout, 75)


        self.verticalLayout = QVBoxLayout(self)

        self.openFileButton = QPushButton("OpenFile")
        self.openFolderButton = QPushButton("OpenFolder")
        self.deleteFileButton = QPushButton("DeleteFile")
        self.resetButton = QPushButton("Reset")

        self.verticalLayout.addWidget(self.openFileButton)
        self.verticalLayout.addWidget(self.openFolderButton)
        self.verticalLayout.addWidget(self.deleteFileButton)
        self.verticalLayout.addWidget(self.resetButton)

        self.horizontLayout.addLayout(self.verticalLayout, 10)
        self.setLayout(self.horizontLayout)

        self.scenesListWidget.itemSelectionChanged.connect(self.__tab1SceneSelectionChanged)
        self.filesListWidget.itemSelectionChanged.connect(self.__tab1FileSelectionChanged)


        self.openFileButton.clicked.connect(self.__openFileButtonClick)
        self.openFolderButton.clicked.connect(self.__openFolderButtonClick)
        self.deleteFileButton.clicked.connect(self.__deleteFileButtonClick)
        self.resetButton.clicked.connect(self.__resetButtonClick)


        self.setTabButtonsEnabled(False)


    def setTabButtonsEnabled(self, enable):
        self.openFileButton.setEnabled(enable)
        self.openFolderButton.setEnabled(enable)
        self.deleteFileButton.setEnabled(enable)


    def update(self, project_folder_path=None):
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        self.scenesListWidget.clear()

        def showContent(part_path_scene_tex, part_path_scene_scripts):
            path_to_scenes_texture = os.path.join(self.project_folder_path_, part_path_scene_tex)
            if not os.path.exists(path_to_scenes_texture):
                print('What went wrong!!!!Maybe can not open folder: ' + path_to_scenes_texture)
                return

            for folder_name in os.listdir(path_to_scenes_texture):
                # path = os.path.join(self.project_folder_path_, folder_name)
                path_to_scene_texture = os.path.join(path_to_scenes_texture, folder_name)
                # print('path_to_scene_texture ', path_to_scene_texture)

                if not os.path.isfile(path_to_scene_texture):
                    path_to_scenes_scripts = os.path.join(self.project_folder_path_,
                                                          part_path_scene_scripts,
                                                          folder_name)

                    file_names = self.__getContainsUnusedFiles(path_to_scene_texture, path_to_scenes_scripts)
                    if len(file_names) > 0:
                        self.__addedSceneInfo(folder_name, file_names)
                        self.scenesListWidget.addItem(folder_name)

        showContent(const.PATH_TO_SCENES_TEXTURE, const.PATH_TO_SCENES_SCRIPTS)
        showContent(const.PATH_TO_CE_SCENES_TEXTURE, const.PATH_TO_CE_SCENES_SCRIPTS)



    def __addedSceneInfo(self, folder_name, info):
        self.sceneInfos[folder_name] = info

    def __getSceneInfo(self, folder_name):
        return self.sceneInfos[folder_name]


    def __getContainsUnusedFiles(self, path_to_scenes_texture, path_to_scenes_scripts):
        # print('__getContainsUnusedFiles ' + path_to_scenes_texture, path_to_scenes_scripts)
        file_names = []

        # files_texture = suf.merge(suf.walk_texture(path_to_scenes_texture))
        files_texture = suf.walk_texture(path_to_scenes_texture)
        files_scripts = suf.walk_scripts(path_to_scenes_scripts)

        files_texture_unused = suf.walk(path_to_scenes_scripts, files_scripts, files_texture, self.project_folder_path_)
        # print('files_texture_unused ', files_texture_unused)
        # print('________________________________________________')

        for abs_name in files_texture_unused:
            if os.path.isfile(abs_name):
                file_names.append(abs_name.replace('\\', '/'))


        return file_names

    def __tab1SceneSelectionChanged(self):
        folder_name = self.scenesListWidget.currentItem().text()
        # print('__tab1_scene_selection_changed ' + folder_name)

        files_texture_unused = self.__getSceneInfo(folder_name)

        self.filesListWidget.clear()
        self.setTabButtonsEnabled(False)
        for abs_name in files_texture_unused:
            if os.path.isfile(abs_name):
                self.filesListWidget.addItem(abs_name)


    def __tab1FileSelectionChanged(self):
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


            if self.filesListWidget.count() == 0:
                self.scenesListWidget.takeItem(self.scenesListWidget.currentRow())
                # self.__addedSceneInfo(file_name, None)
        else:
            return

    def __resetButtonClick(self):
        self.scenesListWidget.clear()
        self.filesListWidget.clear()
        self.update()