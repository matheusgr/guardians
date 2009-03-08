import os
import os.path
from tarfile import TarFile

def translate_size(bytes):
    kb = 1024
    mb = 1024 * kb
    gb = 1024 * mb
    tb = 1024 * gb
    if bytes >= tb:
        return (str(bytes / tb), "TB")
    if bytes >= gb:
        return (str(bytes / gb), "GB")
    if bytes >= mb:
        return (str(bytes / mb), "MB")
    if bytes >= kb:
        return (str(bytes / kb), "KB")
    return (str(bytes), "bytes")

class Node:
    def __init__(self, name, size, parent):
        self.name = name
        self.size = size
        self.parent = parent
        self.child = []
        self.is_dir = False

    def is_root(self):
        return self.parent == None

    def __rstr(self, size):
        result = ''
        result += self.name + ' ' + str(self.size) + '\n'
        for c in self.child:
            print c
            result += size*' ' + Node.__rstr(c, size + 2)
        return result

    def __repr__(self):
        return self.__rstr(0)
        

def _recursive_list(base_dir, current, parent):
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
        child = Node(current, size, parent)
        parent.child.append(child)
        return size
    else:
        # ignoring unknow type
        return 0
    dir_child = Node(current, 0, parent)
    dir_child.is_dir = True
    for d in listdir:
        dir_child.size += _recursive_list(ffile, d, dir_child)
    parent.child.append(dir_child)
    dir_child.child.sort(key = lambda x: x.size, reverse=True)
    return dir_child.size

def get_list(directory):
    root = Node(directory, 0, None)
    _recursive_list(directory, '', root)
    root.child[0].name = directory # True first directory
    return root

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
