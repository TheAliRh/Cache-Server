from fastapi import FastAPI
import uvicorn
import httpx

from contextlib import asynccontextmanager

from app.api.endpoints.admin import AdminEndpoints
from app.api.endpoints.url import URLEndpoints
from app.api.endpoints.authentication import AuthEndpoints
from app.config import settings
from database.connection import Connection


# Lifespan method
@asynccontextmanager
async def lifespan(app: FastAPI):

    # On startup
    app.state.mongo_client = Connection.mongo_db_manager
    app.state.mongo_client.connect()
    app.state.redis_client = Connection.redis_db_manager
    app.state.redis_client.connect()
    app.state.http_client = httpx.AsyncClient()

    # Yield back to caller
    yield

    # On shutdown
    app.state.mongo_client.disconnect()
    app.state.redis_client.disconnect()


# Define the app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

# Mounting the router
admin_router = AdminEndpoints()
auth_router = AuthEndpoints()
url_shortner_router = URLEndpoints()

app.include_router(router=admin_router)
app.include_router(router=url_shortner_router)
app.include_router(router=auth_router)


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
