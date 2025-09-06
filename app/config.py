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

    # Postgres configuration
    P_HOST = "localhost"
    P_PORT = "5432"
    P_DATABASE = ""
    P_USERNAME = os.getenv("POSTGRS_USERNAME")
    P_PASSWORD = os.getenv("POSTGRS_PASSWORD")
    P_DATABASE_URL = (
        f"postgres://{P_USERNAME}:{P_PASSWORD}@{P_HOST}:{P_PORT}/{P_DATABASE}"
    )


settings = Settings()
