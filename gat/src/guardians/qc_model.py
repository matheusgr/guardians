#!/usr/bin/env python

import os, rquota

STATUS_EXCEPT = -1
STATUS_OK = 1
STATUS_NOQUOTA = 2
STATUS_EPERM = 3

# Model: [host, disk, status, values]
# where "values" is defined at rquota structure (see unpack_rquota at rquota.py)
class QuotaCheckModel:
    
    def __init__(self, hosts):
        self.uid = os.getuid()
        self.hosts = hosts

    def _getList(self, host, disk, status, value):
        value_list = []
        value_list.append(host)
        value_list.append(disk)
        value_list.append(status)
        value_list.append(value)
        return value_list
    
    def getQuota(self):
        result = []
        for host, disk in self.hosts:
            try:
                (status, value) = rquota.getQuotaTCP(host, disk, self.uid)
                if status == STATUS_OK:
                    result.append(self._getList(host,disk,status,value))
                else:
                    result.append(self._getList(host,disk,status,()))
            except:
                result.append(self._getList(host,disk,STATUS_EXCEPT,()))
        return result

class QuotaCheckModelTest(QuotaCheckModel):

    def getQuota(self):
        result = []
        result.append(self._getList('host1', 'home', STATUS_OK, range(7,1,-1)))
        result.append(self._getList('host1', 'tmp', STATUS_OK,  range(7,1,-1)))
        result.append(self._getList('host2', 'bck', STATUS_OK,  range(7,1,-1)))
        result.append(self._getList('host3', 'bck', STATUS_NOQUOTA,()))
        return result
        
            
def main():
    print QuotaCheckModelTest([('coisafofa','/home'), ('seulunga','/home')]).getQuota()
    print QuotaCheckModel([('coisafofa','/home'), ('seulunga','/home')]).getQuota()

if __name__ == "__main__":
    main()
