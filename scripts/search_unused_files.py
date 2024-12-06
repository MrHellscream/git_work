import sys
import os
import re 


def merge(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res


def walk_texture(directory):
    files = []
    if os.path.exists(directory):
        #print('directory ', directory, os.path.basename(directory))
        basename = os.path.basename(directory)
        if not re.search(r'.+_all\b', basename):
            for name in os.listdir(directory):
                path = os.path.join(directory, name)
                path = os.path.normpath(path)

                if os.path.isfile(path):
                    #print('path ', path)
                    files.append(path)
                elif name != 'Animations':
                    #print('name', name)
                    files.extend(walk_texture(path))
    return files


def walk_scripts(directory):
    #print('walk_scripts', directory)
    files = []

    def isLuaAnimFile(name):
        return re.search(r'.+_Anim.lua\b', name) #(name.rfind('_Anim.lua') == -1)
    
    if os.path.exists(directory):
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isfile(path) and not isLuaAnimFile(name): 
                files.append(path)
    else:
        name = directory + '.lua'
        if os.path.isfile(name) and not isLuaAnimFile(name):
            files.append(name)
    
    return files



def get_realpath(abs_name, project_folder_path):
    realpath = os.path.relpath(abs_name, start=project_folder_path).replace('\\', '/')
    return realpath


def walk(directory, files_scripts, files_texture, project_folder_path):
    pattern_true = []
    files_texture_copy = list(files_texture)

    #print(files_scripts, files_texture) 

    for fileScript in files_scripts:
        name = os.path.join(directory, fileScript)
        try:
            data = str(open(name, 'rb').read())
            for abs_name in files_texture_copy:

                realpath = get_realpath(abs_name, project_folder_path)

                if data.find(realpath) != -1:
                    pattern_true.append(abs_name)
                else:
                    pass

            for patternName in pattern_true:
                files_texture_copy.remove(patternName)

        except OSError:
            print('What went wrong!!!!Maybe can not open or read file: ' + name)
            return None
        finally:
            pattern_true = []
    return files_texture_copy
