"""This module is for managing the redis database."""

from redis.asyncio import Redis


class RedisDatabaseManager:

    def __init__(self, host, port, password, db_name):
        self.host = host
        self.port = port
        # self.username = username
        self.password = password
        self.db_name = db_name

    def connect(self, host, port, password, db_name):
        self.client = Redis(self.host, self.port, self.password, self.db_name)

    def disconnect(self):
        self.client.close()

    def set_value(self, key, value, expire):
        self.client.set(key, value, expire)
        return True

    def get_value(self, key):
        self.client.get(key)
        return True

    def delete_value(self, key):
        self.client.delete(key)
        return True

    def exists(self, key):
        return bool(self.client.exists(key))
