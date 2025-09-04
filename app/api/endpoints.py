from fastapi import APIRouter, Request, HTTPException, status
from redis import Redis
import httpx

import json


# Define the endpoint router
router = APIRouter()


@router.get("/entries")
async def get_item(request: Request):

    # Defining the Redis client
    redis_client: Redis = request.app.state.redis

    # Defining the HTTP Client
    http_client: httpx.AsyncClient = request.app.state.http_client

    value = redis_client.get("entries")

    # Check cache miss
    if value is None:

        try:

            # Get API response
            response = await http_client.get("http://ip-api.com/json", timeout=5.0)
            value = response.json()
            data_str = json.dumps(value)

            # Cache the response with expiration
            redis_client.set("entries", data_str, ex=60)

            return value

        # Handling API fetch error
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail=f"Could not fetch API:{str(e)}",
            )

    # Return the API response in json
    return json.loads(value)
