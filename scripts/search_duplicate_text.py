import os
import re
import fileinput

regex = re.compile(r"(?P<key>^.+)=(?P<text>(.+))")

text = "{key}=$({value})"  #


def remove_chars_translate_bytes(subj, chars):
    return subj.translate(None, ''.join(chars))


def find_duplicate(file):
    candidate_dict = {}

    for textLine in file:
        try:
            result = regex.search(textLine)
            key, text = result.group('key'), result.group('text')
        except AttributeError:
            pass
        else:
            # print(key, text)
            if not re.search(r'\A\$\(', text):
                text = text.replace('\\t', '').replace('\\n', ' ')

                if text in candidate_dict:
                    candidate_dict[text]['count'] += 1
                    candidate_dict[text]['keys'].append(key)
                else:
                    candidate_dict[text] = {'count': 1, 'keys': [key]}

    result = {k: v for k, v in candidate_dict.items() if v['count'] != 1}

    return result


def replaceLineInFile(file_name, choose_key, duplicate_keys):
    # print(file_name, choose_key, duplicate_keys)
    with fileinput.FileInput(file_name, inplace=True) as file:
        for line in file:
            line = line.rstrip()  # remove trailing (invisible) space

            try:
                result = regex.search(line)
                key = result.group('key')
            except AttributeError:
                print(line)
            else:
                d_keys = list(duplicate_keys)
                if key in d_keys:
                    print(text.format(key=key, value=choose_key))
                    duplicate_keys.remove(key)
                else:
                    print(line)

