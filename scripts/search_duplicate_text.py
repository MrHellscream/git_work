
import re
import fileinput

# Regular expression to match key-value pairs
regex = re.compile(r"(?P<key>^.+)=(?P<text>(.+))")

# Template for replacement
text_template = "{key}=$({value})"

def remove_chars(subj, chars):
    """
    Removes specified characters from a string.

    Args:
        subj (str): Input string.
        chars (str): Characters to remove.

    Returns:
        str: Cleaned string.
    """
    return subj.translate(str.maketrans('', '', chars))

def find_duplicates(file):
    """
    Finds duplicate text values in a file.

    Args:
        file (iterable): Iterable of file lines.

    Returns:
        dict: Dictionary with duplicate text as keys and occurrence info as values.
    """
    candidate_dict = {}

    for line in file:
        match = regex.search(line)
        if not match:
            continue

        key, value = match.group('key'), match.group('text')

        if not re.match(r'\A\$\(', value):
            value = value.replace('\\t', '').replace('\\n', ' ')

            if value in candidate_dict:
                candidate_dict[value]['count'] += 1
                candidate_dict[value]['keys'].append(key)
            else:
                candidate_dict[value] = {'count': 1, 'keys': [key]}

    return {k: v for k, v in candidate_dict.items() if v['count'] > 1}


def replace_line_in_file(file_name, choose_key, duplicate_keys):
    """
    Replaces duplicate text occurrences in a file with a chosen key.

    Args:
        file_name (str): Path to the file.
        choose_key (str): Key to use as the replacement reference.
        duplicate_keys (set): Set of duplicate keys to replace.
    """
    # with fileinput.FileInput(file_name, inplace=True) as file:
    #     for line in file:
    #         match = regex.search(line)
    #         if match:
    #             key = match.group('key')
    #             if key in duplicate_keys:
    #                 print(text_template.format(key=key, value=choose_key))
    #                 duplicate_keys.remove(key)
    #                 continue
    #         print(line, end='')


    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        match = regex.search(line)
        if match:
            key = match.group('key')
            if key in duplicate_keys:
                new_line = text_template.format(key=key, value=choose_key)
                new_lines.append(new_line + "\n" if not new_line.endswith("\n") else new_line)
                duplicate_keys.remove(key)
                continue
        new_lines.append(line)

    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)