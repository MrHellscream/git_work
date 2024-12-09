from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class TabWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.project_folder_path_ = None

        # GUI Tab
        self.horizontLayout = QHBoxLayout(self)

        self.verticalLayout = QVBoxLayout(self)


    def setTabButtonsEnabled(self, enable):
        pass

    def update(self, project_folder_path=None):
        pass





class TabFilesWidget(TabWidget):
    def __init__(self, parent):
        TabWidget.__init__(self, parent)

        self._createCustomGUI()

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

        self.openFileButton.clicked.connect(self.__openFileButtonClick)
        self.openFolderButton.clicked.connect(self.__openFolderButtonClick)
        self.deleteFileButton.clicked.connect(self.__deleteFileButtonClick)
        self.resetButton.clicked.connect(self.__resetButtonClick)

        self.setTabButtonsEnabled(False)

    def _createCustomGUI(self):
        pass

    def setTabButtonsEnabled(self, enable):
        TabWidget.setTabButtonsEnabled(self, enable)

        self.openFileButton.setEnabled(enable)
        self.openFolderButton.setEnabled(enable)
        self.deleteFileButton.setEnabled(enable)

    def _openFileButtonCustomClick(self):
        pass

    def __openFolderButtonCustomClick(self):
        pass

    def __deleteFileButtonCustomClick(self):
        pass

    def __resetButtonCustomClick(self):
        pass


    def __openFileButtonClick(self):
        self._openFileButtonCustomClick()

    def __openFolderButtonClick(self):
        self._openFolderButtonCustomClick()

    def __deleteFileButtonClick(self):
        self._deleteFileButtonCustomClick()

    def __resetButtonClick(self):
        self._resetButtonCustomClick()
