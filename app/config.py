import os


class Settings:

    # FastAPI configuration
    PROJECT_NAME = "Cache Server"
    Project_VERSION = "V 0.2"

    # Redis configuration
    R_HOST = "localhost"
    R_PORT = 6379

    # Uvicorn configuration
    U_HOST = "0.0.0.0"
    U_PORT = 8000
    U_RELOAD = True


settings = Settings()
