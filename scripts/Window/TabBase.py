from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.project_folder_path_ = None

        # GUI Layouts
        self.horizontalLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()
        # self.horizontalLayout.addLayout(self.verticalLayout)

    def set_tab_buttons_enabled(self, enable):
        pass

    def update(self, project_folder_path=None):
        pass


class TabFilesWidget(TabWidget):
    def __init__(self, parent):
        TabWidget.__init__(self, parent)

        self._create_custom_gui()

        self.openFileButton = QPushButton("OpenFile")
        self.openFolderButton = QPushButton("OpenFolder")
        self.deleteFileButton = QPushButton("DeleteFile")
        self.resetButton = QPushButton("Reset")

        self.verticalLayout.addWidget(self.openFileButton)
        self.verticalLayout.addWidget(self.openFolderButton)
        self.verticalLayout.addWidget(self.deleteFileButton)
        self.verticalLayout.addWidget(self.resetButton)

        self.horizontalLayout.addLayout(self.verticalLayout, 10)
        self.setLayout(self.horizontalLayout)

        self.openFileButton.clicked.connect(self.__open_file_button_click)
        self.openFolderButton.clicked.connect(self.__open_folder_button_click)
        self.deleteFileButton.clicked.connect(self.__delete_file_button_click)
        self.resetButton.clicked.connect(self.__reset_button_click)

        self.set_tab_buttons_enabled(False)

    def _create_custom_gui(self):
        pass

    def set_tab_buttons_enabled(self, enable):
        TabWidget.set_tab_buttons_enabled(self, enable)

        self.openFileButton.setEnabled(enable)
        self.openFolderButton.setEnabled(enable)
        self.deleteFileButton.setEnabled(enable)

    def _open_file_button_custom_click(self):
        pass

    def _open_file_button_custom_click(self):
        pass

    def _delete_file_button_custom_click(self):
        pass

    def _reset_button_custom_click(self):
        pass


    def __open_file_button_click(self):
        self._open_file_button_custom_click()

    def __open_folder_button_click(self):
        self._open_folder_button_custom_click()

    def __delete_file_button_click(self):
        self._delete_file_button_custom_click()

    def __reset_button_click(self):
        self._reset_button_custom_click()



class TabTextWidget(TabWidget):
    def __init__(self, parent):
        TabWidget.__init__(self, parent)

        self._create_custom_gui()

        self.chooseTextButton = QPushButton("Choose as primary")
        self.resetButton = QPushButton("Reset")

        self.verticalLayout.addWidget(self.chooseTextButton)
        self.verticalLayout.addWidget(self.resetButton)

        self.horizontalLayout.addLayout(self.verticalLayout, 10)
        self.setLayout(self.horizontalLayout)

        self.chooseTextButton.clicked.connect(self.__choose_text_button_click)
        self.resetButton.clicked.connect(self.__reset_button_click)

        self.set_tab_buttons_enabled(False)

    def _create_custom_gui(self):
        pass

    def set_tab_buttons_enabled(self, enable):
        TabWidget.set_tab_buttons_enabled(self, enable)

        self.chooseTextButton.setEnabled(enable)


    def _choose_text_button_custom_click(self):
        pass

    def _reset_button_custom_click(self):
        pass


    def __choose_text_button_click(self):
        self._choose_text_button_custom_click()

    def __reset_button_click(self):
        self._reset_button_custom_click()
