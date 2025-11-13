import os


class Settings:

    # FastAPI configuration
    PROJECT_NAME = "URL Shortener Server"
    PROJECT_VERSION = "V 0.5"

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

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWTsecretKEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)


settings = Settings()
