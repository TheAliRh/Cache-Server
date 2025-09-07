from fastapi import FastAPI
from redis import Redis
import uvicorn
import httpx

from contextlib import asynccontextmanager

from api.endpoints import router
from config import settings


# Lifespan method
@asynccontextmanager
async def lifespan(app: FastAPI):

    # On startup
    app.state.redis = Redis(host=settings.R_HOST, port=settings.R_PORT)
    app.state.http_client = httpx.AsyncClient()

    # Yield back to caller
    yield

    # On shutdown
    app.state.redis.close()


# Define the app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

# Mounting the router
app.include_router(router=router)


# Health check endpoint
@app.get("/")
async def health_check():
    return {"message": "the server is running!"}


# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.U_HOST,
        port=settings.U_PORT,
        reload=settings.U_RELOAD,
    )
