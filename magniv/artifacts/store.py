import inspect
import os
from datetime import datetime
from typing import Optional

import redis


class MagnivStore:
    """
    It's a wrapper around a Redis connection that provides a few convenience methods for storing and
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
        self.artifacts = []
        self.catalog = []
        try:
            self.r = (
                redis.from_url(os.environ.get("redis_url"))
                if "redis_url" in os.environ
                else redis.Redis(host=host, port=port, db=db)
            )
        except redis.exceptions.ConnectionError as e:
            print("Could not connect to Redis server")
            raise e

    def add_artifact(self, key: str):
        """
        The function takes in a key and adds it to the artifacts list. If the key is not in the list, it
        creates a new dictionary with the key and metadata. If the key is in the list, it adds the
        metadata to the dictionary

        Args:
          key (str): the key of the artifact
        """
        redis_function_name = inspect.stack()[1][3]
        if all(key not in d for d in self.artifacts):
            key_dict = {"key": key, "metadata": []}
        if len(self.artifacts) > 0:
            if a_dict := [a_dict for a_dict in self.artifacts if a_dict["key"] == key]:
                if redis_function_name not in [
                    b_dict["redis_action"] for b_dict in a_dict[0]["metadata"]
                ]:
                    a_dict[0]["metadata"].append(
                        {
                            "redis_action": redis_function_name,
                            "count": 1,
                            "timestamps": [datetime.now()],
                        }
                    )
                else:
                    for b_dict in a_dict[0]["metadata"]:
                        if b_dict["redis_action"] == redis_function_name:
                            b_dict["count"] += 1
                            b_dict["timestamps"].append(datetime.now())
            else:
                key_dict["metadata"].append(
                    {
                        "redis_action": redis_function_name,
                        "count": 1,
                        "timestamps": [datetime.now()],
                    }
                )
                self.artifacts.append(key_dict)
        else:
            key_dict["metadata"].append(
                {"redis_action": redis_function_name, "count": 1, "timestamps": [datetime.now()]}
            )
            self.artifacts.append(key_dict)

    def spop(self, key: str):
        """
        `spop` is a function that removes a value from a set

        Args:
          key (str): The key of the set to remove a random element from.
          description (Optional[str]): Optional[str]
        """
        self.r.spop(key)
        self.add_artifact(key=key)

    def sadd(self, key: str, value: str):
        """
        `sadd` is a function that adds a value to a set

        Args:
          key: The key to store the value in
          value: The value to be added to the set.
        """
        self.r.sadd(key, value)
        self.add_artifact(key=key)

    def srem(self, key: str, value: str):
        """
        It removes a value from a set.

        Args:
          key: The key of the set to remove the value from
          value: The value to be added to the set.
        """
        self.r.srem(key, value)
        self.add_artifact(key=key)

    def sismember(self, key: str, value: str):
        """
        `sismember` checks if a value is a member of a set

        Args:
          key: The key of the set
          value: The value to be added to the set.
        """
        self.r.sismember(key, value)
        self.add_artifact(key=key)

    def scard(self, key: str):
        """
        This function returns the number of elements in the set stored at key

        Args:
          key: The key of the set to get the cardinality of.
        """
        self.r.scard(key)
        self.add_artifact(key=key)
