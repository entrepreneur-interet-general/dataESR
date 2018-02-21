import ConfigParser

class ConfigDatabase(object):
    def __init__(self, filename):
        parser = ConfigParser.RawConfigParser()
        parser.read(filename)
        config_dbs = {}
        sections = parser.sections()
        if len(sections) != 0:
            params = map(lambda s: (s, parser.items(s)), sections)
            for p in params:
                config_dbs[p[0]] = dict(p[1])
            self.config_dbs = config_dbs
        else:
            raise Exception('Config file empty, no sections found.')
    def get_config(self, section):
        return self.config_dbs[section]
