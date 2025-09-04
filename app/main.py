from fastapi import FastAPI
from redis import Redis
import httpx

from contextlib import asynccontextmanager

from app.config import settings


# Lifespan method
@asynccontextmanager
async def lifespan(app: FastAPI):

    # On startup
    app.state.redis = Redis(host=settings.HOST, port=settings.PORT)
    app.state.http_client = httpx.AsyncClient()

    # Yield back to caller
    yield

    # On shutdown
    app.state.redis.close()


# Define the app
app = FastAPI(lifespan=lifespan)
