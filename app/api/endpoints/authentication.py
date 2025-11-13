from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId

from app.utils import password_hash
from database.connection import Connection
from database.mongo.collection_manager import CollectionManager
from models.user import UserDoc
from models.auth import RegisterRequest, LoginRequest
from app.utils.jwt import create_access_token


class AuthEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/authentication", tags=["Authentication"])

        self.mongodb_manager = Connection.mongo_db_manager

        self.__include_routes()

    def __include_routes(self):
        self.post("/login")(self.route_email_login)
        self.post("/register")(self.route_register)

    async def route_email_login(self, body: OAuth2PasswordRequestForm = Depends()):
        """
        Description:
        - This endpoint is used for logging in user

        Args:
        - body: It includes 'username' and 'password'.
            * username: Is used to keep email address of user
            * password: Is used to keep password of user
        """

        email = body.username
        password = body.password

        # No empty input
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

        # Get user info
        query = {"email": email}

        user = await self.mongodb_manager.find_one(
            collection_name=CollectionManager.users, query=query
        )

        # Verify user's password
        if password_hash.verify_password(
            password=password, hashed_password=user["hashed_password"]
        ):

            # Return JWT's access token
            token = create_access_token({"sub": email})

            return {
                "access_token": token,
                "token_type": "bearer",
            }

        else:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The email or password is incorrect!",
            )

    async def route_register(self, body: RegisterRequest):
        """
        Description:
        - This endpoint is used for registering the user.

        Args:
        - body: It include 'email' and 'password'.
            * email: Keeps user's email as it is unique
            * password: Keeps user's password
        """

        email = body.email
        password = body.password

        # No empty input
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

        # Hash password for security
        hashed_password = password_hash.hash_password(password)

        # Adds user to database in UserDoc format
        user_document = UserDoc(
            _id=mongodb_id, email=email, hashed_password=hashed_password, linked_urls=[]
        )

        response = await self.mongodb_manager.insert_doc(
            collection_name=CollectionManager.users, document=user_document.dict()
        )

        # Return JWT's access token
        token = create_access_token({"sub": email})

        return {
            "access_token": token,
            "token_type": "bearer",
        }
