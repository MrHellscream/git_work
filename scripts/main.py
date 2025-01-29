import sys
# import os
# import logging

# from window import MainWindow
# from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget, QAction
import window



if __name__ == '__main__':

    # file_script = 'C:/GrandMaStudiosWork_temp/Projects/MCF_28\assets/Scripts/Items/_Interactive/0_mytime_00_int.lua'
    # print(file_script.rfind('02_drone_flashdrive_03' + '.lua'))
    # file_script = 'SCENE_END_OF_SURVEY_STORY_1'
    # print(file_script.isupper())
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
