from fastapi import APIRouter, HTTPException, status

from datetime import datetime
from bson import ObjectId

from models.url import URLDoc, URLInput, CodeInput
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

    async def route_create_shortened_url(self, original_url: URLInput):

        if original_url == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The URL cannot be empty!",
            )

        checker = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls,
            query={"original_url": str(original_url.url)},
        )

        if checker == None:

            mongodb_id = ObjectId()

            code = generate_url_hash_id(mongodb_id)

            document = URLDoc(
                _id=mongodb_id,
                code=code,
                original_url=str(original_url.url),
                created_at=datetime.utcnow(),
                expires_in_seconds=None,
                clicks=0,
            )
            await mongodb_manager.insert_doc(
                collection_name=CollectionManager.shortened_urls,
                document=document.dict(),
            )

            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail=f"The URL '{code}' got created successfully!",
            )

        else:

            raise HTTPException(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                detail=f"The URL '{checker["code"]}' got created successfully!",
            )

    async def route_update_shortened_url(
        self, code: CodeInput, new_code: CodeInput, original_url: URLInput
    ):

        if code or new_code or original_url == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The field cannot be empty!",
            )

        checker = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls, query={"code": new_code}
        )

        if checker == None:

            document = URLDoc(
                _id=id,
                code=new_code,
                original_url=str(original_url.url),
                created_at=datetime.utcnow(),
                expires_in_seconds=None,
                clicks=0,
            )
            await mongodb_manager.update_one(
                collection_name=CollectionManager.shortened_urls,
                query={"code": code},
                document={"$set": dict(document)},
            )
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED, detail="The URL got updated"
            )

        else:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The URL code {new_code} is already in use!",
            )

    async def route_delete_shortened_url(self, code: CodeInput):

        if code == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The code cannot be empty!",
            )

        query = {"code": code}
        response = await mongodb_manager.delete_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )
        if response != 1:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is a conflict in the process!",
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f"The URL {code} deleted successfully!",
            )

    async def route_get_shortened_url(self, code: CodeInput):

        if code == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The code cannot be empty!",
            )

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

        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=str(response))

    async def route_get_user_profile(self, user_id: ObjectId):

        if user_id == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user id cannot be empty!",
            )

        query = {"_id": user_id}

        user_doc = await mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=query
        )

        user_data_pack += dict(user_doc)

        raise HTTPException(status_code=status.HTTP_200_OK, detail=user_data_pack)

    async def route_get_all_user_urls(self, user_id: ObjectId):

        if user_id == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user id cannot be empty!",
            )

        id_query = {"_id": user_id}

        user_doc = await mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=id_query
        )

        user_urls = []

        for url_code in user_doc["linked_urls"]:

            url_code_query = {"code": url_code}

            url_doc = await mongodb_manager.find_one(
                collection_name=CollectionManager.users, query=url_code_query
            )

        user_urls.append(url_doc)

        raise HTTPException(status_code=status.HTTP_200_OK, detail=user_urls)
