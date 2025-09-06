import os


class Settings:

    # Redis configuration
    R_HOST = "localhost"
    R_PORT = 6379

    # Uvicorn configuration
    U_HOST = "0.0.0.0"
    U_PORT = 8000
    U_RELOAD = True


settings = Settings()
