from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from bson import ObjectId

from app.utils import password_hash
from database.connection import Connection
from database.mongo.collection_manager import CollectionManager
from models.user import UserDoc


class AuthEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/authentication", tags=["Authentication"])

        self.mongodb_manager = Connection.mongo_db_manager

        self.__include_routes()

    def __include_routes(self):
        self.post("/login")(self.route_email_login)
        self.post("/register")(self.route_register)

    async def route_email_login(self, email: EmailStr, password: str):

        if email == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email field cannot be empty!",
            )

        if password == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password field cannot be empty!",
            )

        query = {"email": email}

        user = await self.mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=query
        )

        input_pass = password_hash.hash_password(password)

        if input_pass == user["hashed_password"]:

            return RedirectResponse(url="profile")

        else:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The email or password is incorrect!",
            )

    async def route_register(self, email: EmailStr, password: str):

        if email == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email field cannot be empty!",
            )

        if password == None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password field cannot be empty!",
            )

        mongodb_id = ObjectId()

        hashed_password = password_hash.hash_password(password)

        user_document = UserDoc(
            _id=mongodb_id,
            email=email,
            password=hashed_password,
        )

        response = await self.mongodb_manager.insert_doc(
            collection_name=CollectionManager.users, document=user_document
        )

        return RedirectResponse(url="landing")
