import os


class Settings:

    # FastAPI configuration
    PROJECT_NAME = "Cache Server"
    PROJECT_VERSION = "V 0.2"

    # Redis configuration
    R_HOST = "localhost"
    R_PORT = 6379

    # Uvicorn configuration
    U_HOST = "0.0.0.0"
    U_PORT = 8000
    U_RELOAD = True

    # Mongodb configuration
    M_HOST = "localhost"
    M_PORT = "27017"
    M_DATABASE = "url_shortener"
    M_USERNAME = os.getenv("MONGO_USERNAME")
    M_PASSWORD = os.getenv("MONGO_PASSWORD")
    M_DATABASE_URL = (
        f"mongodb://{M_USERNAME}:{M_PASSWORD}@{M_HOST}:{M_PORT}/{M_DATABASE}"
    )


settings = Settings()
