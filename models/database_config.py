import pymongo
import os
import certifi

mongo = pymongo.MongoClient(os.getenv("DB_URL"), tlsCAFile=certifi.where())
mongodb = mongo.boxit

