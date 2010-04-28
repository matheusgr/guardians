import ConfigParser

QUOTAS_SEC = 'quotas'

class Config:
    def __init__(self, config_file='gat.conf'):
        self.config_file = config_file
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.config_file)

    def getQuotasMap(self):
        result = {}
        for opt, value in self.config.items(QUOTAS_SEC):
            opts = value.split(':')
            host = opts[0]
            disk = opts[1]
            mount = opts[2]
            result[(host, disk)] = mount
        return result

if __name__ == '__main__':
    print Config().getQuotasMap()
