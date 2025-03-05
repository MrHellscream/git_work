import os
import re


def walk_texture(directory):
    """
    Recursively collects file paths from a texture directory, excluding '_all' directories.

    Args:
        directory (str): Path to the texture directory.

    Returns:
        list: List of file paths.
    """
    files = []

    if not os.path.exists(directory):
        return files

    basename = os.path.basename(directory)
    if basename.endswith('_all'):
        return files

    for entry in os.scandir(directory):
        path = os.path.normpath(entry.path)
        if entry.is_file():
            files.append(path)
        elif entry.is_dir() and entry.name != 'Animations':
            files.extend(walk_texture(path))

    return files


# def walk_scripts(directory, exclude_patterns=None):
#     """
#     Collects Lua script files while filtering out unwanted patterns.
#
#     Args:
#         directory (str): Path to the script directory.
#         exclude_patterns (list, optional): List of substrings to exclude files.
#     Returns:
#         list: List of Lua script file paths.
#     """
#     files = []
#     # exclude_patterns = ["Table.lua", "List.lua", "_Anim.lua", "_Dialog_", "_Zoom_", "Animation", "MovieScreen"]
#
#     if not os.path.exists(directory):
#         name = directory + '.lua'
#         if os.path.isfile(name) and not any(pattern in name for pattern in exclude_patterns):
#             files.append(name)
#         return files
#
#     for entry in os.scandir(directory):
#         if entry.is_file() and entry.name.endswith(".lua") and not any(
#                 pattern in entry.name for pattern in exclude_patterns):
#             files.append(entry.path)
#
#     return files


def get_real_path(abs_name, project_folder_path):
    """
    Converts an absolute path to a relative project path with normalized separators.

    Args:
        abs_name (str): Absolute file path.
        project_folder_path (str): Project root directory.

    Returns:
        str: Normalized relative path.
    """
    return os.path.normpath(os.path.relpath(abs_name, start=project_folder_path)).replace('\\', '/')


def walk(directory, files_scripts, files_texture, project_folder_path):
    """
    Identifies unused texture files by checking references in script files.

    Args:
        directory (str): Path to the script directory.
        files_scripts (list): List of script file paths.
        files_texture (list): List of texture file paths.
        project_folder_path (str): Project root directory.

    Returns:
        list: List of unused texture file paths.
    """
    unused_textures = set(files_texture)

    for file_script in files_scripts:
        script_path = os.path.join(directory, file_script)

        try:
            with open(script_path, 'r', encoding='utf-8', errors='ignore') as script_file:
                data = script_file.read()

                used_textures = {texture for texture in unused_textures if
                                 get_real_path(texture, project_folder_path) in data}
                unused_textures.difference_update(used_textures)
        except OSError:
            print(f"Error: Unable to open or read file: {script_path}")
            return None

    return list(unused_textures)