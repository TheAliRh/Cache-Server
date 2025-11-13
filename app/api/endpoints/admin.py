from fastapi import APIRouter, HTTPException, Depends, status

from datetime import datetime
from bson import ObjectId

from models.url import (
    URLDoc,
    URLSummery,
    CreateURLRequest,
    UpdateURLRequest,
    DeleteURLRequest,
    GetURLRequest,
)
from models.user import GetUserRequest
from app.utils.url_hash_generator import generate_url_hash_id
from database.mongo.collection_manager import CollectionManager
from database.connection import Connection
from app.utils.dependencies import get_current_user

mongodb_manager = Connection.mongo_db_manager


class AdminEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/admin", tags=["Admin"])
        self.__include_routes()

    def __include_routes(self):
        self.post(
            "/create_shortened_url",
            status_code=status.HTTP_201_CREATED,
            response_model=str,
        )(self.route_create_shortened_url)
        self.put(
            "/update_shortened_url",
            status_code=status.HTTP_200_OK,
            response_model=str,
        )(self.route_update_shortened_url)
        self.delete(
            "/delete_shortened_url",
            status_code=status.HTTP_200_OK,
            response_model=str,
        )(self.route_delete_shortened_url)
        self.get(
            "/get_shortened_url",
            status_code=status.HTTP_200_OK,
            response_model=URLDoc,
        )(self.route_get_shortened_url)
        self.get(
            "/profile",
            status_code=status.HTTP_200_OK,
            response_model=list,
        )(self.route_get_user_profile)
        self.get(
            "/all_short_urls",
            status_code=status.HTTP_200_OK,
            response_model=list,
        )(self.route_get_all_user_urls)

    async def route_create_shortened_url(
        self, body: CreateURLRequest, current_user: str = Depends(get_current_user)
    ):
        """
        Description:
        This endpoints creates shortened url for user.

        Args:
        - body: Includes 'original_url' and 'code' for creation of shortened url.
            * original_url: the url which the shortened link redirects to it.
            * code: the custom code which user prefers to use. the codes are unique for each original_url.

        """

        original_url = body.original_url
        code = body.code
        expire_time = body.expire_time

        # Check for acceptable code
        if (
            await mongodb_manager.find_one(
                collection_name=CollectionManager.shortened_urls, query={"code": code}
            )
            != None
        ):

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="The custom code already exists",
            )

        # Check for empty original_url input
        if original_url.url == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The URL cannot be empty!",
            )

        # Chech for existance of original_url
        checker = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls,
            query={"original_url": str(original_url.url)},
        )

        if checker == None:

            mongodb_id = ObjectId()

            # No custom code
            if code == None:

                code = generate_url_hash_id(mongodb_id)

            # Format the database object
            document = URLDoc(
                _id=mongodb_id,
                code=code,
                original_url=str(original_url.url),
                created_at=datetime.utcnow(),
                expires_in_seconds=None,
                clicks=0,
            )

            # Insert to database
            await mongodb_manager.insert_doc(
                collection_name=CollectionManager.shortened_urls,
                document=document.dict(),
            )

            return f"The URL '{code}' got created successfully!"

        else:

            return f"The URL '{checker["code"]}' got created successfully!"

    async def route_update_shortened_url(
        self,
        body: UpdateURLRequest,
        current_user: str = Depends(get_current_user),
    ):
        """
        Description:
        This endpoint updates shortened urls

        Args:
        - body: It has 2 variables, 'code' and 'new_code'.
            * code: Takes the current code
            * new_code: Takes the new soon-to-be code

        """

        code = body.current_code
        new_code = body.new_code

        # No empty input accepted
        if code or new_code == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The field cannot be empty!",
            )

        # Check for new_code availablity
        checker = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls, query={"code": new_code}
        )

        if checker == None:

            # Find current code
            if (
                await mongodb_manager.find_one(
                    collection_name=CollectionManager.shortened_urls,
                    query={"code": code},
                )
                == None
            ):

                # Update code to new_code
                await mongodb_manager.update_one(
                    collection_name=CollectionManager.shortened_urls,
                    query={"code": code},
                    document={"$set": {"code": new_code}},
                )
                return "The URL got updated"

            else:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The {code} not found!",
                )

        else:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The URL code {new_code} is already in use!",
            )

    async def route_delete_shortened_url(
        self, body: DeleteURLRequest, current_user: str = Depends(get_current_user)
    ):
        """
        Description:
        This endpoint is used to remove the shortened url.

        Args:
        - body: It take 'code'as input which is the code of shortened url.
        """

        code = body.code

        # No empty input
        if code == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The code cannot be empty!",
            )

        # Check the existance of the code
        if (
            await mongodb_manager.find_one(
                collection_name=CollectionManager.shortened_urls, query={"code": code}
            )
            == None
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"The {code} not found!"
            )

        # Delete the shortened_url
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

            return (f"The URL {code} deleted successfully!",)

    async def route_get_shortened_url(
        self, body: GetURLRequest, current_user: str = Depends(get_current_user)
    ):
        """
        Description:
        This endpoint gets the stats of user's url.

        Args:
        - body: Includes 'code' of shortened url.
            * code: Is used for getting shortened urls stats.
        """

        code = body.code

        # No empty input
        if code == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The code cannot be empty!",
            )

        # Get code info
        query = {"code": code}
        url_status = await mongodb_manager.find_one(
            collection_name=CollectionManager.shortened_urls, query=query
        )

        # Return url's stats
        response = URLDoc(
            _id=url_status["_id"],
            code=url_status["code"],
            original_url=url_status["original_url"],
            created_at=url_status["created_at"],
            expires_in_seconds=url_status["expires_in_seconds"],
            clicks=url_status["clicks"],
        )

        return response

    async def route_get_user_profile(
        self,
        body: GetUserRequest,
        current_user: str = Depends(get_current_user),
    ):
        """
        Description:
        This endpoints gets the user profile info.

        Args:
        - body: Includes '_id' which is the user_id.
            * _id: Is used to find user info.
        """

        user_id = body._id

        # No empty input
        if user_id == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user id cannot be empty!",
            )

        # Find user info
        query = {"_id": ObjectId(user_id)}

        user_doc = await mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=query
        )

        # Return user info
        user_data_pack = []

        user_data_pack.append(dict(user_doc))

        return user_data_pack

    async def route_get_all_user_urls(
        self, body: GetUserRequest, current_user: str = Depends(get_current_user)
    ):
        """
        Description:
        This endpoint gives a summery of all related urls to the user.

        Args:
        - body: Includes '_id' which is the user_id.
            * _id: Is used to find related urls of user.
        """

        user_id = body._id

        # No empty input accepted
        if user_id == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user id cannot be empty!",
            )

        # Get user document
        id_query = {"_id": ObjectId(user_id)}

        user_doc = await mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=id_query
        )

        user_urls = []

        # Get and return summery of urls
        for url_code in user_doc["linked_urls"]:

            url_code_query = {"code": url_code}

            url_doc = await mongodb_manager.find_one(
                collection_name=CollectionManager.users, query=url_code_query
            )

            url_summery = URLSummery(
                code=url_doc["code"],
                clicks=url_doc["clicks"],
            )

            user_urls.append(url_summery)

        return user_urls
