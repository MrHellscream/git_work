import sys
import os



def merge(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res


def walk_texture(directory):
    files = []
    if os.path.exists(directory):
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            path = os.path.normpath(path)

            if os.path.isfile(path):
                # print('path ', path)
                files.append(path)
            elif name != 'Animations':
                 files.extend(walk_texture(path))
    return files


def walk_scripts(directory):
    files = []
    if os.path.exists(directory):
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isfile(path) and (name.rfind('_Anim') == -1):
                files.append(path)
    return files


def get_basename(abs_name):
    name = os.path.splitext(os.path.basename(abs_name))[0]
    return name


def walk(directory, files_scripts, files_texture):
    pattern_true = []
    files_texture_copy = list(files_texture)

    for fileScript in files_scripts:
        name = os.path.join(directory, fileScript)
        try:
            data = str(open(name, 'rb').read())
            for abs_name in files_texture_copy:
                basename = get_basename(abs_name)

                if data.find(basename) != -1:
                    pattern_true.append(abs_name)
                else:
                    pass

            for patternName in pattern_true:
                files_texture_copy.remove(patternName)
        except Exception:
            print('What went wrong!!!!Maybe can not open or read file: ' + name)
            return None
        finally:
            pattern_true = []
    return files_texture_copy