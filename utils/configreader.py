import configparser

reader = configparser.ConfigParser()
reader.read("config.ini")

DB_CONFIG = reader['DB_CONFIG']

def getdbconnectionstring():
    return DB_CONFIG['CONNECTION_STRING']