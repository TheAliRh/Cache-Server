"""This module is used to connect to the databases."""

from database.mongo.mongo_database_manager import MongoDatabaseManager
from database.redis.redis_database_manager import RedisDatabaseManager
from app.config import settings


class Connection:

    mongo_db_manager = MongoDatabaseManager(
        host=settings.M_HOST,
        port=settings.M_PORT,
        username=settings.M_USERNAME,
        password=settings.M_PASSWORD,
        db_name=settings.M_DATABASE,
    )
    redis_db_manager = RedisDatabaseManager(
        host=settings.R_HOST,
        port=settings.R_PORT,
        password=settings.R_PASSWORD,
        db_name=settings.R_DATABASE,
    )
