#!/usr/bin/env python3
"""
This module defines the Cache class for storing and retrieving data in Redis.
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be wrapped by the decorator.

    Returns:
        Callable: The wrapped method with a call count increment.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function increments the call count & calls original method.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The return value of the original method.
        """
        # Increment call count using the method's qualified name as the key
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class for interacting with Redis to store and retrieve data.

    Attributes:
        _redis (redis.Redis): Redis client instance used for data storage.
    """

    def __init__(self):
        """
        Initializes the Cache class by creating a Redis client instance
        and flushing the database to ensure a clean slate.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()
        print("connecting to redis")

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored in Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(
       self,
       key: str,
       fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis by the given key and applies an
        optional conversion function.

        Args:
            key (str): The key to look up in Redis.
            fn (Callable, optional): A function to convert the data.
                                         Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The data stored in Redis,
                                                potentially converted by fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves a stored value from Redis as a UTF-8 decoded string.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            Optional[str]: The stored value decoded as a string,
                           or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves a stored value from Redis as an integer.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            Optional[int]: The stored value converted to an integer,
                           or None if the key does not exist.
        """
        return self.get(key, int)
"""
