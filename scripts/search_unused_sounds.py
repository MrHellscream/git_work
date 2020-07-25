import sys, os


#
#
# ROOT_PATH=os.path.abspath(os.getcwd()).replace('\\dist', '')
#
# pathToScenesScripts   = [ ROOT_PATH + '\\assets\\Scripts\\',
#                           ROOT_PATH + '\\assets\\ExtraGameplay\\Scripts\\',
#                           ROOT_PATH + '\\assets\\ExtraContent\\Scripts'
#                         ]
#
# pathToSounds          = [ ROOT_PATH + '\\assets\\Sound\\Scenes\\00_Common',
#                           ROOT_PATH + '\\assets\\Sound\\Common',
#                           ROOT_PATH + '\\assets\\Sound\\AmbientSounds'
#                         ]
#
# sounds  = []
# scripts = []
#
# def merge(lst, res=[]):
#     res = []
#     for el in lst:
#         res += merge(el) if isinstance(el, list) else [el]
#     return res
#


def merge(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge(el, res) if isinstance(el, list) else res.append(el)
    return res


def getSoundNames(dir):
    sounds = []
    if os.path.exists(dir):
        sounds = os.listdir(dir)

    else:
        print('What went wrong!!!!Maybe can not open folder: ' + dir)

    return sounds


def getScriptNames(dir):
    files = []
    if os.path.exists(dir):
        for name in os.listdir(dir):

            path = os.path.join(dir, name)
            # and (name.rfind('.lua') <> -1)
            if os.path.isfile(path):
                if name.rfind('_Anim') == -1 and \
                   name != 'SoundsList.lua' and \
                   name.rfind('_Dialog_') == -1:
                    files.append(path)

            elif os.path.isdir(path):
                files.append(getScriptNames(path))
    else:
        print('What went wrong!!!!Maybe can not open folder: ' + dir)

    return files


def fixedPattern(pattern_name):
    pattern_name = '\'' + pattern_name.replace('.ogg', '') + '\''
    return pattern_name



def walk(files_scripts, files_sounds):
    pattern_true = []
    files_sounds_copy = list(files_sounds)
    for file_script in files_scripts:
        try:
            data = open(file_script,'rb').read()
            for patternName in files_sounds_copy:
                pattern = fixedPattern(patternName)
                if data.find(pattern) != -1:
                    pattern_true.append(patternName)
                else:
                    pass
            for patternName in pattern_true:
                files_sounds_copy.remove(patternName)
            pattern_true = []

        except OSError:
            print('What went wrong!!!!Maybe can not open file: ' + file_script)
            return None
    return files_sounds_copy
#
# print 'Start search unused sounds:\n'
# try:
#     for path in pathToScenesScripts:
#         scripts.append(GetScripts(path))
#     scripts = merge(scripts)
#
#     for path in pathToSounds:
#         sounds.append(GetSounds(path))
#     sounds = merge(sounds)
#
#     filesSoundsUnused = walk(scripts, sounds)
#     if len(filesSoundsUnused) > 0:
#         for fileSoundsUnused in filesSoundsUnused:
#             print fileSoundsUnused
#     else:
#         print '\nHaha, lucky, nothing found.'
# except OSError:
#     print 'What went wrong!!!!'
# finally:
#     print '\nFinish search unused sounds.'
# raw_input()
