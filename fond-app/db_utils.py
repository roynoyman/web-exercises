from pymongo import MongoClient
from validations import validate_dict_filter

# mongodb
client = MongoClient('localhost', 27017)
db = client.flask_db
cashbacks = db.cashbacks
events = db.events


def insert_one_cb(cashback_dict):
    cashbacks.insert_one(cashback_dict)
    return


def list_cashbacks():
    return list(cashbacks.find({}))


def list_cashbacks_with_filter(filter):
    validate_dict_filter(filter)
    return list(cashbacks.find(filter))


def post_event(event):
    events.insert_one({"_id": event._id, "events": [event.type]})
    # events.update_one(filter={'_id': event._id}, update={"$push": {"events": event.type}}, upsert=True)
    return event._id


def update_event(event):
    events.update_one(filter={'_id': event._id}, update={"$push": {"events": event.type}}, upsert=True)
    return event._id


def get_event_history():
    all_events = list(events.find({}))
    return all_events


def get_event_history_with_filter(filter):
    validate_dict_filter(filter)
    return list(events.find(filter))
    # events.update_one({'cashback_id': event['cashback_id']}, {"$set": event})
