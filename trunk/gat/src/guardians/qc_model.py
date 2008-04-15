#!/usr/bin/env python

import os, rquota

# Model: [host, disk, status, values]
# where "values" is defined at rquota structure (see unpack_rquota at rquota.py)
class QuotaCheckModel:
    def __init__(self):
        self.uid = os.getuid()
        self.hosts = [('coisafofa','/home'), ('seulunga','/home')]
    
    def __getList(self, host, disk, status, value):
        value_list = list(value)
        value_list.insert(0, host)
        value_list.insert(1, disk)
        value_list.insert(2, status)
        return value_list
    
    def getQuota(self):
        result = []
        for host, disk in self.hosts:
            try:
                (status, value) = rquota.getQuotaTCP(host, disk, self.uid)
                if status == rquota.STATUS_OK:
                    result.append(self.__getList(host,disk,status,value))
                else:
                    result.append(self.__getList(host,disk,status,()))
            except:
                result.append(self.__getList(host,disk,rquota.STATUS_EXCEPT,()))
        return result
            
def main():
    print QuotaCheckModel().getQuota()

if __name__ == "__main__":
    main()