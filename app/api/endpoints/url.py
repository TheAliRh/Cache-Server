from fastapi import APIRouter, Request

import httpx

from app.api.endpoints.admin import AdminEndpoints
from database.mongo.collection_manager import CollectionManager


class URLEndpoints(APIRouter):

    def __init__(self):
        super().__init__(prefix="/url", tags=["URL"])
        self.__include_routes()

    def __include_routes(self):
        self.get(f"/page")(self.route_get_shortened_url)

    async def route_get_shortened_url(self, url_code, request: Request):

        admin = AdminEndpoints()

        response = await admin.route_get_shortened_url(
            CollectionManager.shortened_urls, url_code
        )

        self.http_client: httpx.AsyncClient = request.app.state.http_client

        http_site = await self.http_client.get(response, timeout=8.0)

        return {
            "url": response,
            "status": http_site.status_code,
            "headers": dict(http_site.headers),
            "content": http_site.text,
        }
