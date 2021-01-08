from pymongo import MongoClient


def get_mongo_collection():
    client = MongoClient('localhost', 27017)
    db = client.jmBotDB
    collection = db.crawled_URLs
    return collection