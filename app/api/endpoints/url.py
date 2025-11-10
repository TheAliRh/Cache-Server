from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from redis import Redis

import httpx
import json

from models.url_shorten import URLDoc
from database.mongo.collection_manager import CollectionManager
from database.connection import Connection


class URLEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/url", tags=["URL"])
        self.__include_routes()

    def __include_routes(self):
        self.get("/{code}")(self.route_redirect_shortened_url)

    async def route_redirect_shortened_url(self, code, request: Request):

        mongodb_manager = Connection.mongo_db_manager

        self.redis_client = request.app.state.redis_client

        self.http_client: httpx.AsyncClient = request.app.state.http_client

        await mongodb_manager.update_one(
            collection_name=CollectionManager.shortened_urls,
            query={"code": code},
            document={"$inc": {"clicks": 1}},
        )

        value = await self.redis_client.get_value(code)

        if value is None:

            query = {"code": code}
            url_status = await mongodb_manager.find_one(
                collection_name=CollectionManager.shortened_urls, query=query
            )

            data_str = json.dumps({"original_url": url_status["original_url"]})

            await self.redis_client.set_value(code, data_str, expire=60)

            return RedirectResponse(
                url=url_status["original_url"],
                status_code=status.HTTP_308_PERMANENT_REDIRECT,
            )

        else:

            return RedirectResponse(url=value["original_url"])
