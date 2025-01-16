import os


def merge(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge(el, res) if isinstance(el, list) else res.append(el)
    return res


def getItemNames(dir):
    items = {}
    if os.path.exists(dir):
        item_names = os.listdir(dir)
        # print(item_names)
        items = dict((os.path.splitext(item_name)[0], os.path.join(dir, item_name)) for item_name in item_names if not os.path.isfile(os.path.join(dir, item_name)))
    else:
        print('What went wrong!!!!Maybe can not open folder: ' + dir)

    return items


def getScriptNames(dir):
    files = []
    if os.path.exists(dir):
        for name in os.listdir(dir):

            path = os.path.join(dir, name)
            # and (name.rfind('.lua') <> -1)
            if os.path.isfile(path):
                if name.rfind('_Anim.lua') == -1 and \
                    name != 'ItemList.lua' and \
                    name.rfind('_Dialog_') == -1 and \
                    name.rfind('_Zoom_') == -1:
                    files.append(path)

            elif os.path.isdir(path):
                files.append(getScriptNames(path))
    else:
        print('What went wrong!!!!Maybe can not open folder: ' + dir)

    return files


def walk(files_scripts, items):
    found_items = []

    items_copy = dict.copy(items)

    item_names = items_copy.keys()

    for file_script in files_scripts:
        try:
            with open(file_script) as f:
                for num, line in enumerate(f, start=1):
                    for item_name in item_names:
                        if file_script.rfind(item_name + '.lua') > 0:
                            # print(file_script, item_name + '.lua', file_script.rfind(item_name + '.lua'))
                            continue
                        if item_name in line:
                            found_items.append(item_name)
                            # if item_name == '01_mytime_00_int':
                            #     print(file_script)
        except OSError:
            print('What went wrong!!!!Maybe can not open file: ' + file_script)


        for found_item_name in found_items:
            if items_copy.get(found_item_name):
                items_copy.pop(found_item_name)
        found_items = []

    return items_copy
#
# print 'Start search unused items:\n'
# try:
#     for path in pathToScenesScripts:
#         scripts.append(GetScripts(path))
#     scripts = merge(scripts)
#
#     for path in pathToItems:
#         items.append(GetItems(path))
#     items = merge(items)
#
#     filesItemsUnused = walk(scripts, items)
#     if len(filesItemsUnused) > 0:
#         for fileItemsUnused in filesItemsUnused:
#             print fileItemsUnused
#     else:
#         print '\nHaha, lucky, nothing found.'
# except OSError:
#     print 'What went wrong!!!!'
# finally:
#     print '\nFinish search unused items.'
# raw_input()
