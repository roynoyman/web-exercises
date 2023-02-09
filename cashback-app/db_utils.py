from pymongo import MongoClient

# mongodb
client = MongoClient('localhost', 27017)
db = client.flask_db
cashbacks = db.cashbacks


def insert_cashback_to_db(cashback_dict):
    cashbacks.insert_one(cashback_dict)
    return


def list_cashbacks():
    return list(cashbacks.find({}))
