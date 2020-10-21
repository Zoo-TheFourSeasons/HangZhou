import os

from configparser import ConfigParser


DB_MYSQL = 'mysql'
DB_POSTGRES = 'postgres'
DB_DOCKER = 'docker'
DB_LOCAL = 'local'


config = __file__
dir_path = os.path.dirname(os.path.dirname(config))

app_config = ConfigParser()
app_config.read('/'.join((os.path.dirname(config), r'configs.ini')))
