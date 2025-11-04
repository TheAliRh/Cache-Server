from fastapi import APIRouter, Request

import httpx

from admin import AdminEndpoints


class URLEndpoints(APIRouter):

    def __init__(self, request: Request):
        super.__init__(prefix="/url", tags=["URL"])
        self.__include_routes()

        self.http_client: httpx.AsyncClient = request.app.state.http_client

    def __include_routes(self):
        self.get(f"/{self.route_get_shortened_url.url_code}").route_get_shortened_url()

    def route_get_shortened_url(self, url_code, request: Request):

        response = AdminEndpoints.route_get_shortened_url(url_code)

        http_site = self.http_client.get(response, timeout=8.0)

        return http_site
