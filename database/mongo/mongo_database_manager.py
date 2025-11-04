from motor.motor_asyncio import AsyncIOMotorClient

from database.mongo.collection_manager import CollectionManager


class MongoDatabaseManager:

    def __init__(self, host, port, username, password, db_name):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self):
        self.client = AsyncIOMotorClient(
            f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        )

    def disconnect(self):
        self.client.close()

    def insert_one(self, collection_name, document):
        inserted = self.client[collection_name.value].insert_one(document)
        return inserted.insert_id

    def insert_many(self, collection_name, documents):
        inserted_urls = self.client[collection_name.value].insert_many(documents)
        return inserted_urls.inserted_ids

    def find_one(self, collection_name, query):
        shrt_url = self.client[collection_name.value].find_one(query)
        return shrt_url

    def find_many(self, collection_name, query):
        shrt_urls = list[self.client[collection_name.value].find(query)]
        return shrt_urls

    def update_one(self, collection_name, query, document):
        updated_url = self.client[collection_name.value].update_one(query, document)
        return updated_url

    def update_many(self, collection_name, query, documents):
        updated_url = self.client[collection_name.value].update_many(query, documents)
        return updated_url.matched_count, updated_url.modified_count

    def delete_one(self, collection_name, query):
        deleted_url = self.client[collection_name.value].delete_one(query)
        return deleted_url.deleted_count

    def delete_many(self, collection_name, query):
        deleted_urls = self.client[collection_name.value].delete_many(query)
        return deleted_urls.deleted_count
