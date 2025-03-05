import os

def merge(lst):
    """
    Flattens a nested list into a single-level list.

    Args:
        lst (list): Nested list.

    Returns:
        list: Flattened list.
    """
    result = []
    for el in lst:
        if isinstance(el, list):
            result.extend(merge(el))
        else:
            result.append(el)
    return result

def get_files_in_directory(directory, extensions=None, exclude_patterns=None):
    """
    Recursively retrieves files from a directory, optionally filtering by extensions and excluding patterns.

    Args:
        directory (str): Path to the directory.
        extensions (list, optional): List of file extensions to include.
        exclude_patterns (list, optional): List of substrings to exclude files.

    Returns:
        list: List of file paths.
    """
    files = []

    if not os.path.exists(directory):

        name = directory + '.lua'
        if os.path.isfile(name) and not any(pattern in name for pattern in exclude_patterns):
            files.append(name)
        else:
            print(f"Error: Directory '{directory}' does not exist.")
        return files

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)

            if extensions and not any(filename.endswith(ext) for ext in extensions):
                continue

            if exclude_patterns and any(pattern in filename for pattern in exclude_patterns):
                continue

            files.append(filepath)

    return files