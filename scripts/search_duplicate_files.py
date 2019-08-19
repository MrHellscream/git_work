import sys, os


def merge(lst): #res=[]
    res = []
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res


def walk_texture(dir):
    files = []
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        path = os.path.normpath(path)
        if os.path.isfile(path):
            files.append(path)
        elif name != 'Animations':
             files.append(walk_texture(path))
    return files


def walk_scripts(dir):
    files = []
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path) and (name.rfind('_Anim') == -1):
            files.append(path)
    return files


def get_basename(abs_name):
    name = os.path.splitext(os.path.basename(abs_name))[0]
    return name


def walk(dir, files_scripts, files_texture):
    pattern_true = []
    files_texture_copy = list(files_texture)

    for fileScript in files_scripts:
        print(fileScript, files_texture_copy)
        name = os.path.join(dir, fileScript)
        try:
            data = str(open(name, 'rb').read())
            for abs_name in files_texture_copy:
                # print(abs_name)
                basename = get_basename(abs_name)

                # print(basename, ' ', data.find(basename))
                if data.find(basename) != -1:
                    pattern_true.append(abs_name)
                else:
                    pass

            for patternName in pattern_true:
                files_texture_copy.remove(patternName)
        except:
            print('What went wrong!!!!Maybe can not open or read file: ' + name)
            return None
        finally:
            pattern_true = []
    return files_texture_copy