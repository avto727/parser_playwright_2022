import configparser, os
from os import getenv
from utils.custom_errors import ConfigNotFound, EnvNotFound


class AppConfig:
    CONFIG_ENV_NAME = 'MB_ENV'
    CONFIG_DIR = 'C:\\Users\\Xiaomi\\PycharmProjects\\Parser_2022\\parser_playwright_2022\\config'
    # CONFIG_DIR = './configs'

    def __parse_config_env(self):
        return getenv(self.CONFIG_ENV_NAME, None)

    def __get_path_to_config(self, stand_name):
        return f'{self.CONFIG_DIR}\{stand_name}.ini'

    @staticmethod
    def __parse_config_file(path_to_file):
        config = configparser.ConfigParser()
        if len(config.read(path_to_file)) == 0:
            raise ConfigNotFound(path_to_file)
        return config

    def get_config(self):
        stand_name = self.__parse_config_env()
        if stand_name == '' or stand_name is None:
            raise EnvNotFound(self.CONFIG_ENV_NAME)

        path_to_config = self.__get_path_to_config(stand_name)
        config = self.__parse_config_file(path_to_config)
        return config
