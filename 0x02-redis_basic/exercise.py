#!/usr/bin/env python3
"""
This module defines the Cache class for storing and retrieving data in Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for interacting with Redis to store and retrieve data.

    Attributes:
        _redis (redis.Redis): The Redis client instance used for data storage.
    """

    def __init__(self):
        """
        Initializes the Cache class by creating a Redis client instance
        and flushing the database to ensure a clean slate.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
