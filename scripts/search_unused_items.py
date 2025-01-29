import os

def get_item_names(directory):
    """
    Retrieves folder names from a directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        dict: Dictionary of folder names (without extensions) and their paths.
    """
    items = {}

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return items

    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            items[os.path.splitext(name)[0]] = path

    return items

def walk(files_scripts, items):
    """
    Identifies unused items by checking script files for references.

    Args:
        files_scripts (list): List of script file paths.
        items (dict): Dictionary of item names and their paths.

    Returns:
        dict: Dictionary of unused item names and their paths.
    """
    unused_items = items.copy()

    for file_script in files_scripts:
        try:
            with open(file_script, 'r') as script_file:
                script_content = script_file.read()

                for item_name in list(unused_items.keys()):
                    # Skip if the script file name matches item_name.lua
                    if os.path.basename(file_script) == item_name + '.lua':
                        continue

                    if item_name in script_content:
                        unused_items.pop(item_name)
        except OSError as e:
            print(f"Error reading file '{file_script}': {e}")

    return unused_items





# def get_script_names(dir):
#     files = []
#     if os.path.exists(dir):
#         for name in os.listdir(dir):
#
#             path = os.path.join(dir, name)
#             # and (name.rfind('.lua') <> -1)
#             if os.path.isfile(path):
#                 if name.rfind('_Anim.lua') == -1 and \
#                     name != 'ItemList.lua' and \
#                     name.rfind('_Dialog_') == -1 and \
#                     name.rfind('_Zoom_') == -1:
#                     files.append(path)
#
#             elif os.path.isdir(path):
#                 files.append(get_script_names(path))
#     else:
#         print('What went wrong!!!!Maybe can not open folder: ' + dir)
#
#     return files


# def walk(files_scripts, items):
#     found_items = []
#
#     items_copy = dict.copy(items)
#
#     item_names = items_copy.keys()
#
#     for file_script in files_scripts:
#         try:
#             with open(file_script) as f:
#                 for num, line in enumerate(f, start=1):
#                     for item_name in item_names:
#                         if file_script.rfind(item_name + '.lua') > 0:
#                             # print(file_script, item_name + '.lua', file_script.rfind(item_name + '.lua'))
#                             continue
#                         if item_name in line:
#                             found_items.append(item_name)
#                             # if item_name == '01_mytime_00_int':
#                             #     print(file_script)
#         except OSError:
#             print('What went wrong!!!!Maybe can not open file: ' + file_script)
#
#
#         for found_item_name in found_items:
#             if items_copy.get(found_item_name):
#                 items_copy.pop(found_item_name)
#         found_items = []
#
#     return items_copy

