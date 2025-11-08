"""This module is for managing the redis database."""

from redis.asyncio import Redis


class RedisDatabaseManager:

    def __init__(self, host, port, password, db_name):
        self.host = host
        self.port = port
        self.password = password
        self.db_name = db_name

    def connect(self):
        self.client = Redis(
            host=self.host, port=self.port, password=self.password, db=self.db_name
        )

    def disconnect(self):
        self.client.close()

    async def set_value(self, key, value, expire):
        response = await self.client.set(key, value, expire)
        return response

    async def get_value(self, key):
        value = await self.client.get(key)
        return value

    async def delete_value(self, key):
        response = await self.client.delete(key)
        return response

    async def exists(self, key):
        does_exist = await bool(self.client.exists(key))
        return does_exist
