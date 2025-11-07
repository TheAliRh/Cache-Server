from motor.motor_asyncio import AsyncIOMotorClient

from database.mongo.collection_manager import CollectionManager


class MongoDatabaseManager:

    def __init__(self, host, port, username, password, db_name):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        self.client = AsyncIOMotorClient(f"mongodb://{self.host}:{self.port}")
        self.db_name = self.client.db_name

    def disconnect(self):
        self.client.close()

    async def insert_doc(self, collection_name, document):
        inserted = await self.db_name.collection_name.insert_one(document)
        return {"inserted_id": str(inserted.inserted_id)}

    async def insert_many_docs(self, collection_name, documents):
        inserted_urls = await self.db_name.collection_name.insert_many(documents)
        return inserted_urls.inserted_ids

    async def find_one(self, collection_name, query):
        shrt_url = await self.db_name.collection_name.find_one(query)
        return shrt_url

    async def find_many(self, collection_name, query):
        shrt_urls = await list[self.db_name.collection_name.find(query)]
        return shrt_urls

    async def update_one(self, collection_name, query, document):
        updated_url = await self.db_name.collection_name.update_one(query, document)
        return {"updated_url": str(updated_url)}

    async def update_many(self, collection_name, query, documents):
        updated_url = await self.db_name.collection_name.update_many(query, documents)
        return updated_url.matched_count, updated_url.modified_count

    async def delete_one(self, collection_name, query):
        deleted_url = await self.db_name.collection_name.delete_one(query)
        return deleted_url.deleted_count

    async def delete_many(self, collection_name, query):
        deleted_urls = await self.db_name.collection_name.delete_many(query)
        return deleted_urls.deleted_count
