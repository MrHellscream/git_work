import json
import constants as const


def getProjectFolderPathFromConfig(path):
    config_data = {}
    try:
        with open(path) as config_file:
            config_data = json.load(config_file)
    except json.JSONDecodeError:
        print('Upsss ' + const.CONFIG_PATH + ' is empty')

    project_folder_path = config_data.get('projectFolderPath')

    # print(config_data)
    return project_folder_path


def saveProjectFolderPathToConfig(path, value):
    config_data = {'projectFolderPath': value}
    with open(path, 'w') as config_file:
        json.dump(config_data, config_file)


def createConfig(path):
    config_file = open(path, "w")
    config_data = {'projectFolderPath': None}

    json.dump(config_data, config_file)

    config_file.close()