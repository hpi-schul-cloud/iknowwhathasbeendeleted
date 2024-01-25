import logging
import os

from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/scapp')
    client = MongoClient(mongo_url)
    db = client.get_default_database()

    configurable_collections = ['ikwhbd']

    pipeline = [
        {
            '$match': {
                'operationType': 'delete',
                'ns.coll': {'$nin': configurable_collections}
            }
        }
    ]

    with db.watch(pipeline) as stream:
        print("Watching for delete events...")

        for change in stream:
            # Extract relevant information
            collection_name = change['ns']['coll']
            document_id = change['documentKey']['_id']

            print(f"Deletion event in collection '{collection_name}' for document with ID: {document_id}")
            db.ikwhbd.insert_one({
                "source": "iknowwhathasbeendeleted",
                "document_id": document_id,
                "collection": collection_name
            })
