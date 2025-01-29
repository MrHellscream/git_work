import json

def get_project_folder_path_from_config(path):
    """
    Reads the project folder path from the JSON config file.

    Args:
        path (str): Path to the configuration file.

    Returns:
        str: The project folder path if found, or None if not set or file is empty.
    """
    try:
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get('projectFolderPath')
    except FileNotFoundError:
        print(f"Error: Config file '{path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Config file '{path}' is empty or contains invalid JSON.")
    return None


def save_project_folder_path_to_config(path, value):
    """
    Saves the project folder path to the JSON config file.

    Args:
        path (str): Path to the configuration file.
        value (str): The project folder path to save.
    """
    try:
        with open(path, 'w') as config_file:
            json.dump({'projectFolderPath': value}, config_file, indent=4)
    except Exception as e:
        print(f"Error saving project folder path to '{path}': {e}")


def create_config(path):
    """
    Creates a new config file with a default structure if it doesn't exist.

    Args:
        path (str): Path to the configuration file.
    """
    try:
        default_config = {'projectFolderPath': None}
        with open(path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
    except Exception as e:
        print(f"Error creating config file '{path}': {e}")
