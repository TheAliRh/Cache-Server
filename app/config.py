import os


class Settings:

    # FastAPI configuration
    PROJECT_NAME = "URL Shorten-er Server"
    PROJECT_VERSION = "V 0.3"

    # Redis configuration
    R_HOST = "localhost"
    R_PORT = 6379
    R_DATABASE = 0
    R_PASSWORD = ""
    R_DATABASE_URI = f"redis://{R_HOST}:{R_PORT}"

    # Uvicorn configuration
    U_HOST = "0.0.0.0"
    U_PORT = 8000
    U_RELOAD = True

    # Mongodb configuration
    M_HOST = "localhost"
    M_PORT = "27017"
    M_DATABASE = "urlshortener"
    M_USERNAME = os.getenv("MONGO_USERNAME")
    M_PASSWORD = os.getenv("MONGO_PASSWORD")
    M_DATABASE_URI = f"mongodb://{M_USERNAME}:{M_PASSWORD}@{M_HOST}:{M_PORT}"

    # Hash configuration
    HASH_SECRET_KEY = os.getenv("HASH_SECRET_KEY")


settings = Settings()
