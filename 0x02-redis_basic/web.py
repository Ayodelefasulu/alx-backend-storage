#!/usr/bin/env python3
"""
This is cache connects to the web
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()


def cache_result(expiration: int = 10):
    """Decorator to cache the result of a function."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_key = f"cache:{url}"
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # If not cached, get the content and cache it
            content = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, content)
            return content
        return wrapper
    return decorator


def track_access_count(func: Callable) -> Callable:
    """Decorator to track how many times a URL was accessed."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(*args, **kwargs)
    return wrapper


@cache_result(expiration=10)
@track_access_count
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it for 10 seconds."""
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"

    # First access (should take time due to slow response)
    content = get_page(url)
    print(f"First access:\n{content[:100]}...\n")

    # Second access (should be instant due to caching)
    content = get_page(url)
    print(f"Second access (from cache):\n{content[:100]}...\n")

    # Check access count
    access_count = redis_client.get(f"count:{url}").decode('utf-8')
    print(f"Access count: {access_count}")
