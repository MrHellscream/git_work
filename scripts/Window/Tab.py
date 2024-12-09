import os

from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel

from .TabBase import TabFilesWidget

import search_unused_files as suf
import search_unused_sounds as sus

import constants as const


class TabSDFWidget(TabFilesWidget):
    def __init__(self, parent):
        TabFilesWidget.__init__(self, parent)

        self.scene_info = {}

    def _createCustomGUI(self):
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

        self.scenesListWidget.itemSelectionChanged.connect(self.__tab1SceneSelectionChanged)
        self.filesListWidget.itemSelectionChanged.connect(self.__tab1FileSelectionChanged)


    def update(self, project_folder_path=None):
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        self.scenesListWidget.clear()
        self.filesListWidget.clear()

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

        # ------------
        showContent(const.PATH_TO_SCENES_TEXTURE, const.PATH_TO_SCENES_SCRIPTS)
        showContent(const.PATH_TO_CE_SCENES_TEXTURE, const.PATH_TO_CE_SCENES_SCRIPTS)

        showContent(const.PATH_TO_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_INTERACTIVE_ITEM_SCRIPTS)
        showContent(const.PATH_TO_CE_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_CE_INTERACTIVE_ITEM_SCRIPTS)

    def __addedSceneInfo(self, folder_name, info):
        self.scene_info[folder_name] = info

    def __getSceneInfo(self, folder_name):
        return self.scene_info[folder_name]

    def __getContainsUnusedFiles(self, path_to_scenes_texture, path_to_scenes_scripts):
        # print('__getContainsUnusedFiles ' + path_to_scenes_texture, path_to_scenes_scripts)
        file_names = []

        # files_texture = suf.merge(suf.walk_texture(path_to_scenes_texture))
        files_texture = suf.walk_texture(path_to_scenes_texture)
        files_scripts = suf.walk_scripts(path_to_scenes_scripts)
        # print('files_scripts', files_scripts)
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


    def _openFileButtonCustomClick(self):
        print('__openFileButtonCustomClick2')
        current_item = self.filesListWidget.currentItem()
        if current_item:
            path_to_file = current_item.text()
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)

    def _openFolderButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            path_to_file = current_item.text()
            path_to_folder = os.path.split(path_to_file)[0]

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))

    def _deleteFileButtonCustomClick(self):
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

    def _resetButtonCustomClick(self):
        self.scenesListWidget.clear()
        self.filesListWidget.clear()
        self.update()


class TabSDSWidget(TabFilesWidget):
    def __init__(self, parent):
        TabFilesWidget.__init__(self, parent)

        self.sounds_info = {}


    def _createCustomGUI(self):
        self.filesListWidget = QListWidget()
        self.filesListLabel = QLabel('Files')
        self.filesLayout = QVBoxLayout(self)

        self.filesLayout.addWidget(self.filesListLabel, 0)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontLayout.addLayout(self.filesLayout, 75)

        self.filesListWidget.itemSelectionChanged.connect(self.__tab1FileSelectionChanged)

    def update(self, project_folder_path=None):
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        print('tab2 update ' + self.project_folder_path_)
        self.filesListWidget.clear()

        def showContent(path_to_sounds, path_to_scenes_scripts):
            sounds = {}
            script_names = []

            for path in path_to_sounds:
                full_path_to_sounds = os.path.join(self.project_folder_path_, path)
                sounds.update(sus.getSoundNames(full_path_to_sounds))

            # print(sounds)

            for path in path_to_scenes_scripts:
                full_path_to_script = os.path.join(self.project_folder_path_, path)
                script_names.append(sus.getScriptNames(full_path_to_script))

            script_names = sus.merge(script_names)
            # print(script_names)

            unused_sounds = sus.walk(script_names, sounds)
            # print(unused_sounds)

            for sound_name, path in unused_sounds.items():
                # print(sound_name, path)
                self.__addedSoundInfo(sound_name, path)
                self.filesListWidget.addItem(sound_name)

        showContent(const.PATH_TO_SOUNDS, const.PATH_TO_SCRIPTS)




    def __addedSoundInfo(self, sound_name, info):
        self.sounds_info[sound_name] = info

    def __getSoundInfo(self, sound_name):
        return self.sounds_info[sound_name]

    def __tab1FileSelectionChanged(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            self.setTabButtonsEnabled(True)
        else:
            self.setTabButtonsEnabled(False)


    def _openFileButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            sound_name = current_item.text()
            path_to_file = self.__getSoundInfo(sound_name)
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)


    def _openFolderButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            sound_name = current_item.text()
            path_to_file = self.__getSoundInfo(sound_name)
            path_to_folder = os.path.dirname(path_to_file)

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))


    def _deleteFileButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()

        if current_item:
            sound_name = current_item.text()
            path_to_file = self.__getSoundInfo(sound_name)
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


    def _resetButtonCustomClick(self):
        self.filesListWidget.clear()
        self.update()
