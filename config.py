import configparser


class Config(object):
    __config = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__config = configparser.ConfigParser()
            cls.__config.read("config.conf")
            cls.__instance = super(Config, cls).__new__(cls)
        return cls.__instance

    def __getitem__(self, key):
        return Config.__config[key]
