import os
from tarfile import TarFile

def _recursive_list(directory, result):
    try:
        listdir = os.listdir(directory)
    except (OSError):
        size = os.lstat(directory).st_size
        result.append((directory, size))
        return size
    cur_result = []
    size = 0
    for dir in listdir:
        size += _recursive_list(directory + os.sep + dir, cur_result)
    result.append((directory, cur_result, size))
    return size

def get_list(directory):
    result = []
    _recursive_list(directory, result)
    return result

def recursive_delete(directory):
    try:
        listdir = os.listdir(directory)
        for dir in listdir:
            recursive_delete(directory + os.sep + dir)
        os.rmdir(directory)
    except (OSError):
        os.remove(directory)

def compact(directory, dest_file):
    tmpname = os.tmpnam()
    t = TarFile.open(tmpname, "w:bz2")
    t.add(directory)
    t.close()
    os.rename(tmpname, dest_file)
    recursive_delete(directory)
    
def move(old, new):
    os.rename(old, new)