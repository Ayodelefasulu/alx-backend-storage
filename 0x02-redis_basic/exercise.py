#!/usr/bin/env python3
"""
This module returns history of all stored caches
"""
import redis
from typing import Callable, Union, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the count of calls
        self._redis.incr(f"{method.__qualname__}:count")
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Convert the args to a string to store as input
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input args in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method and store the output in Redis
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis and optionally convert it using `fn`."""
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve data as a UTF-8 string."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieve data as an integer."""
        return self.get(key, int)


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_, output in zip(inputs, outputs):
        input_args = input_.decode("utf-8")
        output_val = output.decode("utf-8")
        print(f"{method_name}(*{input_args}) -> {output_val}")


# Testing the implementation
if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)
