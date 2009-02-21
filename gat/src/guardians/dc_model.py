import os
import os.path
from tarfile import TarFile

def _recursive_list(base_dir, current, result):
    """
    List a directory recursively. Result list will return a tree where each
    node represents a directory or a file. When a node is a file, it will
    be a list of two parameters: file name and file size. When a node is a
    directory, it will contains also a list of nodes of given directory.
    """
    ffile = base_dir + os.sep + current
    if os.path.isdir(ffile):
        listdir = os.listdir(ffile)
    elif os.path.isfile(ffile):
        size = os.lstat(ffile).st_size
        result.append([current, size])
        return size
    cur_result = []
    size = 0
    for d in listdir:
        size += _recursive_list(ffile, d, cur_result)
    cur_result.sort(lambda x, y: cmp(x[-1], y[-1])) # Sort by size
    result.append([current, cur_result, size])
    return size

def get_list(directory):
    result = []
    _recursive_list(directory, '.', result)
    result[0][0] = directory
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