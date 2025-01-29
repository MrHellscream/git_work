import sys
import os
import re 



def walk_texture(directory):
    files = []

    if os.path.exists(directory):
        basename = os.path.basename(directory)
        if not re.search(r'.+_all\b', basename):
            for name in os.listdir(directory):
                path = os.path.join(directory, name)
                path = os.path.normpath(path)

                if os.path.isfile(path):
                    files.append(path)
                elif name != 'Animations':
                    files.extend(walk_texture(path))
    return files


def walk_scripts(directory):
    files = []

    pattern = r"^(?!.*(Table\.lua|List\.lua|_Anim\.lua|_Dialog_|_Zoom_|Animation|MovieScreen)).*\.lua$"
    def isNormalLuaFile(file_name):
        # return  re.search(r'.+_Anim.lua\b', file_name) #(name.rfind('_Anim.lua') == -1)
        return re.match(pattern, name)
    
    if os.path.exists(directory):
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            if os.path.isfile(path) and isNormalLuaFile(name):
                files.append(path)
    else:
        name = directory + '.lua'
        if os.path.isfile(name) and isNormalLuaFile(name):
            files.append(name)
    
    return files



def get_real_path(abs_name, project_folder_path):
    real_path = os.path.relpath(abs_name, start=project_folder_path).replace('\\', '/')
    return real_path


def walk(directory, files_scripts, files_texture, project_folder_path):
    pattern_true = []
    files_texture_copy = list(files_texture)

    for fileScript in files_scripts:
        name = os.path.join(directory, fileScript)
        try:
            data = str(open(name, 'rb').read())
            for abs_name in files_texture_copy:

                real_path = get_real_path(abs_name, project_folder_path)

                if data.find(real_path) != -1:
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
