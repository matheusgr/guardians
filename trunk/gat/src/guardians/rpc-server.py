from rpc import UDPServer, TCPServer
import rpc
from rquota import RQUOTAPROG, RQUOTAVERS

rpc.TIMEOUT = 1000 # Loop will last until timeout!

class RQuotaServer(UDPServer):
    def __init__(self, server, quotas=None):
        if quotas == None:
            quotas = {}
            quotas['/home'] = (1, 1024, True, 10000, 8000, 7, 2000, 1000, 200, 0, 0)
            quotas['/tmp'] = (0,)
            quotas['/var/mail'] = (1, 1000, True, 10000, 8000, 9, 2000, 1000, 200, 0, 0)
        self.quotas = quotas
        UDPServer.__init__(self, '', RQUOTAPROG, RQUOTAVERS, 0)
    
    def handle_1(self):
        disk = self.unpacker.unpack_string()
        uid = self.unpacker.unpack_uint()
        self.turn_around()
        if not self.quotas.has_key(disk) or not self.quotas[disk][0]:
            self.packer.pack_enum(0)
            return
        status, bsize, active, bhardlimit, bsoftlimit, curblocks, fhardlimit, \
                fsoftlimit, curfiles, btimeleft, ftimeleft = \
                self.quotas[disk]
        self.packer.pack_enum(status)
        self.packer.pack_int(bsize)
        self.packer.pack_bool(active)
        self.packer.pack_uint(bhardlimit)
        self.packer.pack_uint(bsoftlimit)
        self.packer.pack_uint(curblocks)
        self.packer.pack_uint(fhardlimit)
        self.packer.pack_uint(fsoftlimit)
        self.packer.pack_uint(curfiles)
        self.packer.pack_uint(btimeleft)
        self.packer.pack_uint(ftimeleft)

s = RQuotaServer(UDPServer)

try:
    s.unregister()
except RuntimeError, msg:
    print 'RuntimeError:', msg, '(ignored)'
s.register()
print 'Service started...'
try:
    s.loop()
finally:
    s.unregister()
    print 'Service interrupted.'
