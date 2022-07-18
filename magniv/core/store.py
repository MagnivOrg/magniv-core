import os
from typing import Optional

import redis


class MagnivStore:
    """
    A wrapper around a Redis connection that provides a few convenience methods for storing and
    retrieving data
    """

    def __init__(
        self, port: Optional[int] = 6379, host: Optional[str] = "localhost", db: Optional[int] = 0
    ):
        """
        The function creates a Redis object and assigns it to the variable r.

        :param port: The port number of the Redis server, defaults to 6379 (optional)
        :param host: The hostname of the Redis server, defaults to localhost (optional)
        :param db: The database number to connect to, defaults to 0 (optional)
        """
        try:
            self.r = (
                redis.from_url(os.environ.get("REDIS_URL"))
                if "REDIS_URL" in os.environ
                else redis.Redis(host=host, port=port, db=db)
            )
        except redis.exceptions.ConnectionError as e:
            print("Could not connect to Redis server")
            raise e

    def set(self, key: str, value: str):
        """
        `set` is a function that sets a value to a key

        Args:
          key (str): The key to assign the value to.
          value (str): The value to assign to the key.
        """
        return self.r.set(key, value)

    def get(self, key: str):
        """
        `get` is a function that gets a value from a key

        Args:
          key (str): The key to get the value from.
        """
        value = self.r.get(key)
        if value is not None:
            value = value.decode()
        return value

    def delete(self, key: str):
        """
        `delete` is a function that deletes the value for a key

        Args:
            key (str): The key to delete the value from.
        """
        return self.r.delete(key)

    def spop(self, key: str):
        """
        `spop` is a function that removes a value from a set

        Args:
          key (str): The key of the set to remove a random element from.
        """
        value = self.r.spop(key)
        if value is not None:
            value = value.decode()
        return value

    def sadd(self, key: str, value: str):
        """
        `sadd` is a function that adds a value to a set

        Args:
          key: The key to store the value in
          value: The value to be added to the set.
        """
        return self.r.sadd(key, value)

    def srem(self, key: str, value: str):
        """
        `srem` is a function that removes a value from a set.

        Args:
          key: The key of the set to remove the value from
          value: The value to be removed from the set.
        """
        return self.r.srem(key, value)

    def sismember(self, key: str, value: str):
        """
        `sismember` is a function that checks if a value is a member of a set

        Args:
          key: The key of the set
          value: The value to check if it is a member of the set.
        """
        return self.r.sismember(key, value)

    def scard(self, key: str):
        """
        `scard` is a function that returns the number of elements in the set stored at key

        Args:
          key: The key of the set to get the cardinality of.
        """
        return self.r.scard(key)

    def smembers(self, key: str):
        """
        `smembers` is a function that returns the members of a set

        Args:
         key: The key of the set to retrieve members of.
        """
        values = self.r.smembers(key)
        if values is not None:
            values = {v.decode() for v in values}
        return values
