from datetime import datetime
from pymongo import MongoClient, ReturnDocument
import dns
from logger import logger
import config



def fetch_collection():
    CONNECTION_STRING = config.DB_STRING
    client = MongoClient(CONNECTION_STRING)

    test_db = client['leakie']
    collection = test_db['queries']

    return collection


def insert(search_term):
    collection = fetch_collection()
    document = collection.find_one({'search_term': search_term})

    if document is None:
        today = datetime.today()
        date = f'{today.year}.{today.month}.{today.day}'
        new_doc = {'search_term': search_term, 'users': [], 'date': date}
        collection.insert_one(new_doc)
        logger.info(f"New document has been inserted! ~{search_term}~")


def find_users(search_term):
    collection = fetch_collection()
    users = collection.find_one({'search_term': search_term})['users']
    return users


def update(query, user_id):
    collection = fetch_collection()
    insert(query)
    users = find_users(query)

    if user_id not in users:
        users.append(user_id)

        collection.find_one_and_update({'search_term': query},
                                       {'$set': {'users': users}},
                                       return_document=ReturnDocument.AFTER)
        logger.info(f"Query user list updated - {query} - {user_id}")


def find_search_terms():
    collection = fetch_collection()
    queries = collection.find()
    search_terms = []

    for query in queries:
        search_terms.append(query['search_term'])

    return search_terms


def delete(search_term):
    collection = fetch_collection()
    collection.find_one_and_delete({'search_term': search_term})
    logger.info(f"`{search_term}~ has been deleted from database!")
