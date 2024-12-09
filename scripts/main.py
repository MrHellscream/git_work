# import sys
# import os
# import logging

# from window import MainWindow

import window


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    #
    # project_folder_path = None
    #
    # if os.path.exists(const.CONFIG_PATH):
    #     project_folder_path = confHelper.getProjectFolderPathFromConfig(const.CONFIG_PATH)
    # else:
    #     confHelper.createConfig(const.CONFIG_PATH)
    #
    #
    # if not project_folder_path:
    #     # only folder.
    #     project_folder_path = QFileDialog.getExistingDirectory(None, 'Select project folder:', os.getcwd())
    #
    #     confHelper.saveProjectFolderPathToConfig(const.CONFIG_PATH, project_folder_path)
    #
    #
    # if project_folder_path:
    #     main = Main(project_folder_path)
    #     main.show()
    #     main.update()
    #
    #     sys.exit(app.exec_())

    app = window.StartApp()

    # sys.exit(app.exec_())
