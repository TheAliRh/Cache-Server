from fastapi import APIRouter

from datetime import datetime
from bson import ObjectId

from models.url_shorten import URLDoc, ShortenRequest
from utils.url_hash_generator import generate_url_hash_id
from database.mongo.collection_manager import CollectionManager
from database.connection import Connection

mongodb_manager = Connection.mongo_db_manager


class AdminEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/admin", tags=["Admin"])
        self.__include_routes()

    def __include_routes(self):
        self.post("/create_shortened_url")(self.route_create_shortened_url)
        self.put("/update_shortened_url")(self.route_update_shortened_url)
        self.delete("/delete_shortened_url")(self.route_delete_shortened_url)
        self.get("/get_shortened_url")(self.route_get_shortened_url)

    def route_create_shortened_url(self, original_url):

        mongodb_id = ObjectId()

        code = generate_url_hash_id(mongodb_id)

        document = URLDoc(
            _id=mongodb_id,
            code=code,
            original_url=original_url,
            created_at=datetime.utcnow(),
            expires_in_seconds=None,
            clicks=0,
        )
        response = mongodb_manager.insert_one(
            collection_name=CollectionManager.shortened_urls, document=document
        )

        return response

    def route_update_shortened_url(self, code, original_url):
        document = URLDoc(
            _id=None,
            code=code,
            original_url=original_url,
            created_at=datetime.utcnow(),
            expires_in_seconds=None,
            clicks=0,
        )
        response = mongodb_manager.update_one(
            collection_name=CollectionManager.shortened_urls,
            query={f"original_url:{original_url}"},
            document=document,
        )
        return response

    def route_delete_shortened_url(self, original_url, code):
        query = {
            f"original_url:{original_url}",
            f"code:{code}",
        }
        response = mongodb_manager.delete_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )
        return response

    def route_get_shortened_url(self, code):
        query = {f"code:{code}"}
        response = mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )
        return response
