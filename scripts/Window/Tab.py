import os
import shutil


from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel, QPushButton

from .TabBase import TabFilesWidget, TabTextWidget

import search_unused_files as suf
import search_unused_sounds as sus
import search_duplicate_text as sdw
import search_unused_items as sui

import constants as const
import searchHelpers as sHelpers

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

        self.horizontalLayout.addLayout(self.sceneLayout, 15)
        self.horizontalLayout.addLayout(self.filesLayout, 75)

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
                path_to_scene_texture = os.path.join(path_to_scenes_texture, folder_name)


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

        showContent(const.PATH_TO_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_INTERACTIVE_ITEM_SCRIPTS)
        showContent(const.PATH_TO_CE_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_CE_INTERACTIVE_ITEM_SCRIPTS)


    def __addedSceneInfo(self, folder_name, info):
        self.scene_info[folder_name] = info


    def __getSceneInfo(self, folder_name):
        return self.scene_info[folder_name]


    def __getContainsUnusedFiles(self, path_to_scenes_texture, path_to_scenes_scripts):
        file_names = []

        files_texture = suf.walk_texture(path_to_scenes_texture)
        files_scripts = suf.walk_scripts(path_to_scenes_scripts, exclude_patterns=["_Anim.lua",
                                                                                   "_Dialog_"])

        files_texture_unused = suf.walk(path_to_scenes_scripts, files_scripts, files_texture, self.project_folder_path_)

        for abs_name in files_texture_unused:
            if os.path.isfile(abs_name):
                file_names.append(abs_name.replace('\\', '/'))

        return file_names


    def __tab1SceneSelectionChanged(self):
        folder_name = self.scenesListWidget.currentItem().text()

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


#----------------------------------------------------------------------------------------
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

        self.horizontalLayout.addLayout(self.filesLayout, 75)

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
                sounds.update(sus.get_sound_names(full_path_to_sounds))

            # print(sounds)

            for path in path_to_scenes_scripts:
                full_path_to_script = os.path.join(self.project_folder_path_, path)
                # script_names.append(sus.get_script_names(full_path_to_script))
                script_names.append(sHelpers.get_files_in_directory(full_path_to_script, extensions=[".lua"],
                                                                    exclude_patterns=["_Anim", "_Dialog_", "_Zoom_",
                                                                                      "List.lua", "Table.lua",
                                                                                      "MovieScreen.lua",
                                                                                      "Animations.lua",
                                                                                      "ApplicationManager"]))

            script_names = sHelpers.merge(script_names)
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


#----------------------------------------------------------------------------------------
class TabSDTWidget(TabTextWidget):
    def __init__(self, parent):
        TabTextWidget.__init__(self, parent)

        self.text_info = {}
        self.full_path_to_text = None


    def _createCustomGUI(self):
        self.textValuesListWidget = QListWidget()
        self.textKeysListWidget = QListWidget()

        self.textValuesListLabel = QLabel('Text')
        self.textKeysListLabel = QLabel('Keys')

        self.textValuesLayout = QVBoxLayout(self)
        self.textKeysLayout = QVBoxLayout(self)

        self.textValuesLayout.addWidget(self.textValuesListLabel, 0)
        self.textKeysLayout.addWidget(self.textKeysListLabel, 0)

        self.textValuesLayout.addWidget(self.textValuesListWidget)
        self.textKeysLayout.addWidget(self.textKeysListWidget)

        self.horizontalLayout.addLayout(self.textValuesLayout, 50)
        self.horizontalLayout.addLayout(self.textKeysLayout, 30)

        self.textValuesListWidget.itemSelectionChanged.connect(self.__tab3TextValuesSelectionChanged)
        self.textKeysListWidget.itemSelectionChanged.connect(self.__tab3TextKeysSelectionChanged)


    def update(self, project_folder_path=None):
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        self.textValuesListWidget.clear()
        self.textKeysListWidget.clear()

        print('tab3 update ' + self.project_folder_path_)

        self.full_path_to_text = os.path.join(self.project_folder_path_, const.PATH_TO_TEXT)
        if self.full_path_to_text:
            try:
                open_file = open(self.full_path_to_text, 'r')
            except FileNotFoundError:
                print('Can not open file ' + self.full_path_to_text)
            else:
                self.text_info = sdw.find_duplicates(open_file)

                open_file.close()
                # print(self.text_info )
                for key in self.text_info.keys():
                    self.textValuesListWidget.addItem(key)


    def __tab3TextValuesSelectionChanged(self):
        key = self.textValuesListWidget.currentItem().text()

        values = self.text_info[key]['keys']

        self.textKeysListWidget.clear()
        self.setTabButtonsEnabled(False)

        for textKey in values:
            self.textKeysListWidget.addItem(textKey)


    def __tab3TextKeysSelectionChanged(self):
        current_item = self.textKeysListWidget.currentItem()

        if current_item:
            self.setTabButtonsEnabled(True)
        else:
            self.setTabButtonsEnabled(False)


    def _chooseTextButtonCustomClick(self):
        current_item = self.textKeysListWidget.currentItem()

        if current_item:
            key = self.textValuesListWidget.currentItem().text()
            text_key = self.textKeysListWidget.currentItem().text()

            duplicate_keys = list(self.text_info[key]['keys'])
            duplicate_keys.remove(text_key)

            if self.full_path_to_text:
                sdw.replace_line_in_file(self.full_path_to_text, text_key, duplicate_keys)
                self.textKeysListWidget.clear()
                self.textValuesListWidget.takeItem(self.textValuesListWidget.currentRow())


    def _resetButtonCustomClick(self):
        self.textValuesListWidget.clear()
        self.textKeysListWidget.clear()

        self.update()


#----------------------------------------------------------------------------------------
class TabSUIWidget(TabFilesWidget):
    def __init__(self, parent):
        TabFilesWidget.__init__(self, parent)

        self.items_info = {}

        self.openFileButton.setText('Open Item')
        self.openFolderButton.setText('Open Item Folder')
        self.deleteFileButton.setText('Delete Item')

        self.precacheStaticInfoButton = QPushButton("PrecacheStaticInfo")
        self.verticalLayout.addWidget(self.precacheStaticInfoButton)
        self.precacheStaticInfoButton.clicked.connect(self.__precacheStaticInfoButtonClick)

    def _createCustomGUI(self):
        self.filesListWidget = QListWidget()
        self.filesListLabel = QLabel('Items')
        self.filesLayout = QVBoxLayout(self)

        self.filesLayout.addWidget(self.filesListLabel, 0)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontalLayout.addLayout(self.filesLayout, 75)

        self.filesListWidget.itemSelectionChanged.connect(self.__tab1FileSelectionChanged)


    def update(self, project_folder_path=None):
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        print('tab4 update ' + self.project_folder_path_)
        self.filesListWidget.clear()

        def showContent(path_to_items, path_to_scenes_scripts):
            items = {}
            script_names = []

            for path in path_to_items:
                full_path_to_items = os.path.join(self.project_folder_path_, path)
                items.update(sui.get_item_names(full_path_to_items))
        #
            # print(items)
        #
            for path in path_to_scenes_scripts:
                full_path_to_script = os.path.join(self.project_folder_path_, path)
                # script_names.append(sui.get_script_names(full_path_to_script))

                script_names.append(sHelpers.get_files_in_directory(full_path_to_script, extensions=[".lua"],
                                       exclude_patterns=["_Anim", "_Dialog_", "_Zoom_", "ItemList"]))
        #
            script_names = sHelpers.merge(script_names)
            # print(script_names)
        #
            unused_items = sui.walk(script_names, items)
            # print(unused_items)
        #
            for item_name, path in unused_items.items():
                # print(item_name, path)
                self.__addedItemInfo(item_name, path)
                self.filesListWidget.addItem(item_name)

        showContent(const.PATH_TO_ITEM_TEXTURE, const.PATH_TO_SCENE_SCRIPTS)


    def __addedItemInfo(self, item_name, info):
        self.items_info[item_name] = info


    def __getItemInfo(self, item_name):
        return self.items_info[item_name]


    def __tab1FileSelectionChanged(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            self.setTabButtonsEnabled(True)
        else:
            self.setTabButtonsEnabled(False)


    def _openFileButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            item_name = current_item.text()
            path_to_file = self.__getItemInfo(item_name)
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)


    def _openFolderButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()
        if current_item:
            item_name = current_item.text()
            path_to_file = self.__getItemInfo(item_name)
            path_to_folder = os.path.dirname(path_to_file)

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))


    def _deleteFileButtonCustomClick(self):
        current_item = self.filesListWidget.currentItem()

        if current_item:
            item_name = current_item.text()
            path_to_folder = self.__getItemInfo(item_name)
            if os.path.exists(path_to_folder):
                try:
                    # os.remove(path_to_folder)
                    shutil.rmtree(path_to_folder)

                    for dir in [const.PATH_TO_INTERACTIVE_ITEM_SCRIPTS, const.PATH_TO_CE_INTERACTIVE_ITEM_SCRIPTS]:
                        # print(dir)
                        path_to_file = os.path.join(self.project_folder_path_, dir, item_name)
                        # print(path_to_file)
                        if os.path.exists(path_to_file + '.lua'):
                            os.remove(path_to_file + '.lua')

                        if os.path.exists(path_to_file + '_Anim.lua'):
                            os.remove(path_to_file + '_Anim.lua')
                    #
                    for dir in [const.PATH_TO_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_CE_INTERACTIVE_ITEM_TEXTURE]:
                        path_to_int_folder = os.path.join(self.project_folder_path_, dir, item_name)
                        if os.path.exists(path_to_int_folder):
                            shutil.rmtree(path_to_int_folder)

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

    def __precacheStaticInfoButtonClick(self):
        path_to_precache_static_info = os.path.join(self.project_folder_path_, const.PATH_TO_PRECACHE_STATIC_INFO)
        old_root = os.getcwd()
        os.chdir(os.path.normpath(os.path.dirname(path_to_precache_static_info)))
        os.startfile(os.path.normpath(path_to_precache_static_info))
        os.chdir(old_root)

