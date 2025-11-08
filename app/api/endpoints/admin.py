from fastapi import APIRouter

from datetime import datetime
from bson import ObjectId

from models.url_shorten import URLDoc, ShortenRequest
from app.utils.url_hash_generator import generate_url_hash_id
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

    async def route_create_shortened_url(self, original_url):

        value = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls,
            query={"original_url": original_url},
        )

        if value == None:

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
            response = await mongodb_manager.insert_doc(
                collection_name=CollectionManager.shortened_urls,
                document=document.dict(),
            )

            return code

        else:

            return value["code"]

    async def route_update_shortened_url(self, code, new_code, original_url):
        document = URLDoc(
            _id=id,
            code=new_code,
            original_url=original_url,
            created_at=datetime.utcnow(),
            expires_in_seconds=None,
            clicks=0,
        )
        response = await mongodb_manager.update_one(
            collection_name=CollectionManager.shortened_urls,
            query={"code": code},
            document={"$set": dict(document)},
        )
        return response

    async def route_delete_shortened_url(self, code):
        query = {"code": code}
        response = await mongodb_manager.delete_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )
        return response

    async def route_get_shortened_url(self, code):
        query = {"code": code}
        url_status = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )

        response = URLDoc(
            _id=url_status["_id"],
            code=url_status["code"],
            original_url=url_status["original_url"],
            created_at=url_status["created_at"],
            expires_in_seconds=url_status["expires_in_seconds"],
            clicks=url_status["clicks"],
        )

        return response
