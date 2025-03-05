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

#----------------------------------------------------------------------------------------
class TabSDFWidget(TabFilesWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.scene_info = {}
        # self._create_custom_gui()
        self._setup_connections()


    def _create_custom_gui(self):
        """ Creates the graphical user interface for the widget. """
        self.scenesListWidget = QListWidget()
        self.filesListWidget = QListWidget()

        self.sceneListLabel = QLabel("Scenes")
        self.filesListLabel = QLabel("Files")

        self.sceneLayout = QVBoxLayout()
        self.filesLayout = QVBoxLayout()

        self.sceneLayout.addWidget(self.sceneListLabel)
        self.sceneLayout.addWidget(self.scenesListWidget)

        self.filesLayout.addWidget(self.filesListLabel)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontalLayout.addLayout(self.sceneLayout, 15)
        self.horizontalLayout.addLayout(self.filesLayout, 75)

    def _setup_connections(self):
        """ Binds signals to slots. """
        self.scenesListWidget.itemSelectionChanged.connect(self._scene_selection_changed)
        self.filesListWidget.itemSelectionChanged.connect(self._file_selection_changed)


    def update(self, project_folder_path=None):
        """ Updates the list of scenes and files. """
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        print("TabSDFWidget update: " + self.project_folder_path_)
        self.scenesListWidget.clear()
        self.filesListWidget.clear()

        def show_content(part_path_scene_tex, part_path_scene_scripts):
            path_to_textures = os.path.join(self.project_folder_path_, part_path_scene_tex)
            if not os.path.exists(path_to_textures):
                print(f"Error: Cannot open folder {path_to_textures}")
                return

            for folder_name in os.listdir(path_to_textures):
                path_to_scene_texture = os.path.join(path_to_textures, folder_name)

                if not os.path.isfile(path_to_scene_texture):
                    path_to_scripts = os.path.join(self.project_folder_path_, part_path_scene_scripts, folder_name)
                    file_names = self._get_unused_files(path_to_scene_texture, path_to_scripts)

                    if file_names:
                        self._add_scene_info(folder_name, file_names)
                        self.scenesListWidget.addItem(folder_name)

        paths = [
            (const.PATH_TO_SCENES_TEXTURE, const.PATH_TO_SCENES_SCRIPTS),
            (const.PATH_TO_CE_SCENES_TEXTURE, const.PATH_TO_CE_SCENES_SCRIPTS),
            (const.PATH_TO_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_INTERACTIVE_ITEM_SCRIPTS),
            (const.PATH_TO_CE_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_CE_INTERACTIVE_ITEM_SCRIPTS),
        ]

        for texture_path, script_path in paths:
            show_content(texture_path, script_path)

    def _add_scene_info(self, folder_name, info):
        self.scene_info[folder_name] = info

    def _get_scene_info(self, folder_name):
        return self.scene_info.get(folder_name, [])


    def _get_unused_files(self, path_to_textures, path_to_scripts):
        """ Retrieves a list of unused files. """

        files_texture = suf.walk_texture(path_to_textures)
        files_scripts = sHelpers.get_files_in_directory(
            path_to_scripts, extensions=[".lua"], exclude_patterns=["_Anim", "_Dialog_"]
        )

        unused_files = suf.walk(path_to_scripts, files_scripts, files_texture, self.project_folder_path_)
        return [f.replace("\\", "/") for f in unused_files if os.path.isfile(f)]

    def _scene_selection_changed(self):
        """ Handles scene selection changes. """
        current_item = self.scenesListWidget.currentItem()
        if not current_item:
            return

        folder_name = current_item.text()
        files_texture_unused = self._get_scene_info(folder_name)

        self.filesListWidget.clear()
        self.set_tab_buttons_enabled(False)

        for abs_name in files_texture_unused:
            if os.path.isfile(abs_name):
                self.filesListWidget.addItem(abs_name)

    def _file_selection_changed(self):
        """ Enables buttons if a file is selected. """
        self.set_tab_buttons_enabled(bool(self.filesListWidget.currentItem()))

    def _open_file_button_custom_click(self):
        """ Opens the selected file. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            path_to_file = current_item.text()
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)

    def _open_folder_button_custom_click(self):
        """ Opens the folder containing the selected file. """
        current_item = self.filesListWidget.currentItem()
        if not current_item:
            return

        path_to_folder = os.path.dirname(current_item.text())
        if os.path.exists(path_to_folder):
            try:
                os.startfile(path_to_folder)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}")

    def _delete_file_button_custom_click(self):
        """ Deletes the selected file and updates the list. """
        current_item = self.filesListWidget.currentItem()
        if not current_item:
            return

        path_to_file = current_item.text()
        if os.path.exists(path_to_file):
            try:
                os.remove(path_to_file)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}")
                return

        row = self.filesListWidget.row(current_item)
        self.filesListWidget.takeItem(row)

        if self.filesListWidget.count() == 0:
            self.scenesListWidget.takeItem(self.scenesListWidget.currentRow())

    def _reset_button_custom_click(self):
        """ Clears the lists and refreshes the data. """
        self.scenesListWidget.clear()
        self.filesListWidget.clear()
        self.update()

#----------------------------------------------------------------------------------------
class TabSDSWidget(TabFilesWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.sounds_info = {}

    def _create_custom_gui(self):
        """ Creates the graphical user interface for the widget. """
        self.filesListWidget = QListWidget()
        self.filesListLabel = QLabel("Files")
        self.filesLayout = QVBoxLayout(self)

        self.filesLayout.addWidget(self.filesListLabel, 0)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontalLayout.addLayout(self.filesLayout, 75)

        self.filesListWidget.itemSelectionChanged.connect(self._file_selection_changed)

    def update(self, project_folder_path=None):
        """ Updates the list of unused sound files. """
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        print("TabSDSWidget update: " + self.project_folder_path_)
        self.filesListWidget.clear()

        def show_content(path_to_sounds, path_to_scenes_scripts):
            sounds = {}
            script_names = []

            for path in path_to_sounds:
                full_path_to_sounds = os.path.join(self.project_folder_path_, path)
                sounds.update(sus.get_sound_names(full_path_to_sounds))

            for path in path_to_scenes_scripts:
                full_path_to_script = os.path.join(self.project_folder_path_, path)
                script_names.append(sHelpers.get_files_in_directory(
                    full_path_to_script, extensions=[".lua"],
                    exclude_patterns=["_Anim", "_Dialog_", "_Zoom_",
                                      "List.lua", "Table.lua",
                                      "MovieScreen.lua", "Animations.lua",
                                      "ApplicationManager"]
                ))

            script_names = sHelpers.merge(script_names)
            unused_sounds = sus.walk(script_names, sounds)

            for sound_name, path in unused_sounds.items():
                self._add_sound_info(sound_name, path)
                self.filesListWidget.addItem(sound_name)

        show_content(const.PATH_TO_SOUNDS, const.PATH_TO_SCRIPTS)

    def _add_sound_info(self, sound_name, info):
        """ Stores sound file information. """
        self.sounds_info[sound_name] = info

    def _get_sound_info(self, sound_name):
        """ Retrieves stored sound file path by name. """
        return self.sounds_info.get(sound_name, "")

    def _file_selection_changed(self):
        """ Enables buttons if a file is selected. """
        self.set_tab_buttons_enabled(bool(self.filesListWidget.currentItem()))

    def _open_file_button_custom_click(self):
        """ Opens the selected sound file. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            sound_name = current_item.text()
            path_to_file = self._get_sound_info(sound_name)
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)

    def _open_folder_button_custom_click(self):
        """ Opens the folder containing the selected sound file. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            sound_name = current_item.text()
            path_to_file = self._get_sound_info(sound_name)
            path_to_folder = os.path.dirname(path_to_file)

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}")

    def _delete_file_button_custom_click(self):
        """ Deletes the selected sound file and updates the list. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            sound_name = current_item.text()
            path_to_file = self._get_sound_info(sound_name)
            if os.path.exists(path_to_file):
                try:
                    os.remove(path_to_file)
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}")
                    return
            else:
                print("The file does not exist")

            selected_items = self.filesListWidget.selectedItems()
            for item in selected_items:
                self.filesListWidget.takeItem(self.filesListWidget.row(item))

    def _reset_button_custom_click(self):
        """ Clears the list and refreshes data. """
        self.filesListWidget.clear()
        self.update()

#----------------------------------------------------------------------------------------
class TabSDTWidget(TabTextWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.text_info = {}
        self.full_path_to_text = None

        # self._create_custom_gui()
        self._setup_connections()

    def _create_custom_gui(self):
        """ Creates the graphical user interface for the widget. """
        self.textValuesListWidget = QListWidget()
        self.textKeysListWidget = QListWidget()

        self.textValuesListLabel = QLabel("Text")
        self.textKeysListLabel = QLabel("Keys")

        self.textValuesLayout = QVBoxLayout()
        self.textKeysLayout = QVBoxLayout()

        self.textValuesLayout.addWidget(self.textValuesListLabel)
        self.textValuesLayout.addWidget(self.textValuesListWidget)

        self.textKeysLayout.addWidget(self.textKeysListLabel)
        self.textKeysLayout.addWidget(self.textKeysListWidget)

        self.horizontalLayout.addLayout(self.textValuesLayout, 50)
        self.horizontalLayout.addLayout(self.textKeysLayout, 30)

    def _setup_connections(self):
        """ Binds signals to slots. """
        self.textValuesListWidget.itemSelectionChanged.connect(self._text_values_selection_changed)
        self.textKeysListWidget.itemSelectionChanged.connect(self._text_keys_selection_changed)

    def update(self, project_folder_path=None):
        """ Updates the text duplicates list. """
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        self.textValuesListWidget.clear()
        self.textKeysListWidget.clear()

        print(f"TabSDTWidget update: {self.project_folder_path_}")

        self.full_path_to_text = os.path.join(self.project_folder_path_, const.PATH_TO_TEXT)

        if not self.full_path_to_text or not os.path.exists(self.full_path_to_text):
            print(f"Error: Cannot open file {self.full_path_to_text}")
            return

        with open(self.full_path_to_text, "r") as open_file:
            self.text_info = sdw.find_duplicates(open_file)

        for key in self.text_info.keys():
            self.textValuesListWidget.addItem(key)

    def _text_values_selection_changed(self):
        """ Handles text value selection changes. """
        current_item = self.textValuesListWidget.currentItem()
        if not current_item:
            return

        key = current_item.text()
        values = self.text_info.get(key, {}).get("keys", [])

        self.textKeysListWidget.clear()
        self.set_tab_buttons_enabled(False)

        for text_key in values:
            self.textKeysListWidget.addItem(text_key)

    def _text_keys_selection_changed(self):
        """ Enables buttons if a key is selected. """
        self.set_tab_buttons_enabled(bool(self.textKeysListWidget.currentItem()))

    def _choose_text_button_custom_click(self):
        """ Removes the selected duplicate text key from the file. """
        current_item = self.textKeysListWidget.currentItem()
        if not current_item:
            return

        key = self.textValuesListWidget.currentItem().text()
        text_key = current_item.text()

        duplicate_keys = self.text_info.get(key, {}).get("keys", [])
        if text_key in duplicate_keys:
            duplicate_keys.remove(text_key)

        if self.full_path_to_text:
            sdw.replace_line_in_file(self.full_path_to_text, text_key, duplicate_keys)
            self.textKeysListWidget.clear()
            self.textValuesListWidget.takeItem(self.textValuesListWidget.currentRow())

    def _reset_button_custom_click(self):
        """ Clears the lists and refreshes data. """
        self.textValuesListWidget.clear()
        self.textKeysListWidget.clear()
        self.update()

#----------------------------------------------------------------------------------------
class TabSUIWidget(TabFilesWidget):
    def __init__(self, parent):
        TabFilesWidget.__init__(self, parent)

        self.items_info = {}

        self.openFileButton.setText("Open Item")
        self.openFolderButton.setText("Open Item Folder")
        self.deleteFileButton.setText("Delete Item")

        self.precacheStaticInfoButton = QPushButton("Precache Static Info")
        self.verticalLayout.addWidget(self.precacheStaticInfoButton)

        self._setup_connections()

    def _create_custom_gui(self):
        """ Creates the graphical user interface for the widget. """
        self.filesListWidget = QListWidget()
        self.filesListLabel = QLabel("Items")
        self.filesLayout = QVBoxLayout()

        self.filesLayout.addWidget(self.filesListLabel)
        self.filesLayout.addWidget(self.filesListWidget)

        self.horizontalLayout.addLayout(self.filesLayout, 75)

    def _setup_connections(self):
        """ Binds signals to slots. """
        self.filesListWidget.itemSelectionChanged.connect(self._file_selection_changed)
        self.precacheStaticInfoButton.clicked.connect(self._precache_static_info_button_click)

    def update(self, project_folder_path=None):
        """ Updates the list of unused items. """
        if project_folder_path:
            self.project_folder_path_ = project_folder_path

        print(f"TabSUIWidget update: {self.project_folder_path_}")
        self.filesListWidget.clear()

        def show_content(path_to_items, path_to_scenes_scripts):
            items = {}
            script_names = []

            for path in path_to_items:
                full_path_to_items = os.path.join(self.project_folder_path_, path)
                items.update(sui.get_item_names(full_path_to_items))

            for path in path_to_scenes_scripts:
                full_path_to_script = os.path.join(self.project_folder_path_, path)
                script_names.append(sHelpers.get_files_in_directory(
                    full_path_to_script, extensions=[".lua"],
                    exclude_patterns=["_Anim", "_Dialog_", "_Zoom_", "ItemList"]
                ))

            script_names = sHelpers.merge(script_names)
            unused_items = sui.walk(script_names, items)

            for item_name, path in unused_items.items():
                self._add_item_info(item_name, path)
                self.filesListWidget.addItem(item_name)

        show_content(const.PATH_TO_ITEM_TEXTURE, const.PATH_TO_SCENE_SCRIPTS)

    def _add_item_info(self, item_name, info):
        """ Stores item information. """
        self.items_info[item_name] = info

    def _get_item_info(self, item_name):
        """ Retrieves stored item path by name. """
        return self.items_info.get(item_name, "")

    def _file_selection_changed(self):
        """ Enables buttons if an item is selected. """
        self.set_tab_buttons_enabled(bool(self.filesListWidget.currentItem()))

    def _open_file_button_custom_click(self):
        """ Opens the selected item file. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            item_name = current_item.text()
            path_to_file = self._get_item_info(item_name)
            if os.path.exists(path_to_file):
                os.startfile(path_to_file)

    def _open_folder_button_custom_click(self):
        """ Opens the folder containing the selected item. """
        current_item = self.filesListWidget.currentItem()
        if current_item:
            item_name = current_item.text()
            path_to_file = self._get_item_info(item_name)
            path_to_folder = os.path.dirname(path_to_file)

            if os.path.exists(path_to_folder):
                try:
                    os.startfile(path_to_folder)
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}")

    def _delete_file_button_custom_click(self):
        """ Deletes the selected item and its related files. """
        current_item = self.filesListWidget.currentItem()
        if not current_item:
            return

        item_name = current_item.text()
        path_to_folder = self._get_item_info(item_name)

        try:
            # Delete item folder if it exists
            if os.path.exists(path_to_folder):
                shutil.rmtree(path_to_folder)

            # Delete associated script files
            for dir_path in [const.PATH_TO_INTERACTIVE_ITEM_SCRIPTS, const.PATH_TO_CE_INTERACTIVE_ITEM_SCRIPTS]:
                path_to_script = os.path.join(self.project_folder_path_, dir_path, item_name)
                for ext in [".lua", "_Anim.lua"]:
                    script_file = path_to_script + ext
                    if os.path.exists(script_file):
                        os.remove(script_file)

            # Delete associated textures
            for dir_path in [const.PATH_TO_INTERACTIVE_ITEM_TEXTURE, const.PATH_TO_CE_INTERACTIVE_ITEM_TEXTURE]:
                path_to_texture_folder = os.path.join(self.project_folder_path_, dir_path, item_name)
                if os.path.exists(path_to_texture_folder):
                    shutil.rmtree(path_to_texture_folder)

        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}")
            return

        # Remove selected item from list
        selected_items = self.filesListWidget.selectedItems()
        for item in selected_items:
            self.filesListWidget.takeItem(self.filesListWidget.row(item))


    def _reset_button_custom_click(self):
        """ Clears the list and refreshes data. """
        self.filesListWidget.clear()
        self.update()

    def _precache_static_info_button_click(self):
        """ Runs the precache static info script with directory change. """
        path_to_script = os.path.join(self.project_folder_path_, const.PATH_TO_PRECACHE_STATIC_INFO)
        if os.path.exists(path_to_script):
            try:
                old_root = os.getcwd()
                os.chdir(os.path.normpath(os.path.dirname(path_to_script)))
                os.startfile(os.path.normpath(path_to_script))
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}")
            finally:
                os.chdir(old_root)


