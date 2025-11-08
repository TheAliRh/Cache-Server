from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from redis import Redis

import httpx
import json

from app.api.endpoints.admin import AdminEndpoints
from database.mongo.collection_manager import CollectionManager


class URLEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/url", tags=["URL"])
        self.__include_routes()

    def __include_routes(self):
        self.get("/{url_code}")(self.route_redirect_shortened_url)

    async def route_redirect_shortened_url(self, url_code, request: Request):

        response = await AdminEndpoints.route_get_shortened_url(
            CollectionManager.shortened_urls, url_code
        )

        self.redis_client = request.app.state.redis_client

        self.http_client: httpx.AsyncClient = request.app.state.http_client

        value = await self.redis_client.get_value(url_code)
        if value is None:

            redirect_page = RedirectResponse(url=response)

            data_str = json.dumps(
                {
                    "url": redirect_page.url,
                    "status_code": redirect_page.status_code,
                    "headers": dict(redirect_page.headers),
                }
            )

            await self.redis_client.set_value(url_code, data_str, expire=60)

            return redirect_page

        else:

            return RedirectResponse(url=value)
