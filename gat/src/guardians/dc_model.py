import os

class DiskCleanModel():
    
    def __init__(self, directory):
        self.r = []
        self.recursive_list(directory, self.r)
        print self.r
    
    def recursive_list(self, directory, result):
        try:
            listdir = os.listdir(directory)
        except (OSError):
            size = os.lstat(directory).st_size
            result.append((directory, size))
            return size
        cur_result = []
        size = 0
        for dir in listdir:
            size += self.recursive_list(directory + os.sep + dir, cur_result)
        result.append((directory, cur_result, size))
        return size

    def get_list(self):
        return self.r