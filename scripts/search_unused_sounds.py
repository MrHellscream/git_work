import os


def merge(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge(el, res) if isinstance(el, list) else res.append(el)
    return res


def getSoundNames(dir):
    sounds = {}
    if os.path.exists(dir):
        sound_names = os.listdir(dir)

        sounds = dict((os.path.splitext(sound_name)[0], os.path.join(dir, sound_name)) for sound_name in sound_names)
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


def walk(files_scripts, sounds):
    found_sounds = []

    sounds_copy = dict.copy(sounds)

    sound_names = sounds_copy.keys()

    for file_script in files_scripts:
        try:
            with open(file_script) as f:
                for num, line in enumerate(f, start=1):
                    for sound_name in sound_names:
                        if sound_name in line:
                            found_sounds.append(sound_name)
        except OSError:
            print('What went wrong!!!!Maybe can not open file: ' + file_script)


        for found_sound_name in found_sounds:
            if sounds_copy.get(found_sound_name):
                sounds_copy.pop(found_sound_name)
        found_sounds = []

    return sounds_copy
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
