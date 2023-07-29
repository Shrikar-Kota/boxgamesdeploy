import pymongo
from . import configreader
import certifi

mongo = pymongo.MongoClient(configreader.getdbconnectionstring(), tlsCAFile=certifi.where())
mongodb = mongo.boxit