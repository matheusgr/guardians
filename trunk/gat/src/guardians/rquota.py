import rpc
from rpc import Packer, Unpacker, TCPClient, UDPClient

# file:///usr/include/rpcsvc/rquota.x
RQUOTAPROG = 100011
RQUOTAVERS = 1

STATUS_EXCEPT = -1
STATUS_OK = 1
STATUS_NOQUOTA = 2
STATUS_EPERM = 3

class RQuotaPacker(Packer):
    def pack_getquotaargs(self, sa):
        pathp, uid = sa
        self.pack_string(pathp)
        self.pack_uint(uid)

class RQuotaUnpacker(Unpacker):
    def unpack_rquota(self):
        bsize = self.unpack_int()
        active = self.unpack_bool()
        bhardlimit = self.unpack_uint()
        bsoftlimit = self.unpack_uint()
        curblocks = self.unpack_uint()
        fhardlimit = self.unpack_uint()
        fsoftlimit = self.unpack_uint()
        curfiles = self.unpack_uint()
        btimeleft = self.unpack_uint()
        ftimeleft = self.unpack_uint()
        return (bsize, active, bhardlimit, bsoftlimit, curblocks, fhardlimit, \
                fsoftlimit, curfiles, btimeleft, ftimeleft)
        
    def unpack_rslt(self):
        status = self.unpack_enum()
        if status == 1:
            rquota = self.unpack_rquota()
        else:
            rquota = None
        return status, rquota


class PartialRQuotaClient:

    def addpackers(self):
        self.packer = RQuotaPacker()
        self.unpacker = RQuotaUnpacker('')
    
    def bindsocket(self):
        import os
        try:
            uid = os.getuid()
        except AttributeError:
            uid = 1
        if uid == 0:
            port = rpc.bindresvport(self.sock, '')
            # 'port' is not used
        else:
            self.sock.bind(('', 0))

    def mkcred(self):
        if self.cred == None:
            self.cred = rpc.AUTH_UNIX, rpc.make_auth_unix_default()
        return self.cred

    def Getquota(self, getquotaargs):
        return self.make_call(1, getquotaargs, \
                self.packer.pack_getquotaargs, \
                self.unpacker.unpack_rslt)

    def Getactivequota(self, getquotaargs):
        return self.make_call(2, getquotaargs, \
                self.packer.pack_getquotaargs, \
                self.unpacker.unpack_rslt)

# We turn the partial Mount client into a full one for either protocol
# by use of multiple inheritance.  (In general, when class C has base
# classes B1...Bn, if x is an instance of class C, methods of x are
# searched first in C, then in B1, then in B2, ..., finally in Bn.)
class TCPRQuotaClient(PartialRQuotaClient, TCPClient):

    def __init__(self, host):
        TCPClient.__init__(self, host, RQUOTAPROG, RQUOTAVERS)


class UDPRQuotaClient(PartialRQuotaClient, UDPClient):

    def __init__(self, host):
        UDPClient.__init__(self, host, RQUOTAPROG, RQUOTAVERS)


def getQuotaTCP(host, disk, uid):
    mcl = TCPRQuotaClient(host)
    return mcl.Getquota([disk, uid])

def getQuotaUDP(host, disk, uid):
    mcl = UDPRQuotaClient(host)
    return mcl.Getquota([disk, uid])

def main():
    import sys
    if sys.argv[1:] and sys.argv[1] == '-t':
        C = TCPRQuotaClient
        del sys.argv[1]
    elif sys.argv[1:] and sys.argv[1] == '-u':
        C = UDPRQuotaClient
        del sys.argv[1]
    else:
        C = UDPRQuotaClient
    if sys.argv[1:]: host = sys.argv[1]
    else: host = ''
    mcl = C(host)
    list = mcl.Getquota([sys.argv[2], int(sys.argv[3])])
    print list

if __name__ == "__main__":
    main()