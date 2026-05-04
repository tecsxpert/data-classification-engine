# services/cache_service.py
# Handles Redis caching for AI responses
# Saves AI responses so we don't call Groq repeatedly

import os
import json
import hashlib
import logging
import redis
from datetime import datetime

logger = logging.getLogger(__name__)

# Redis connection
# If Redis is not available we skip caching gracefully
redis_client = None


def get_redis_client():
    """
    Get Redis client connection.
    Returns None if Redis is not available.
    We never crash if Redis is down.
    """
    global redis_client

    try:
        if redis_client is None:
            redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
    socket_connect_timeout=0.5,
    socket_timeout=0.5
)
            # Test connection
            redis_client.ping()
            logger.info("Redis connected successfully!")

        return redis_client

    except Exception as e:
        logger.warning(f"Redis not available: {str(e)}")
        return None


def generate_cache_key(endpoint, data):
    """
    Generate SHA256 cache key from endpoint and data.

    SHA256 = a way to convert any text into
    a unique fixed-length string.

    Example:
    "describe_Customer_DB_email_phone"
    → "a3f5c8b2d9e1..."
    """
    # Create a string from the data
    cache_string = f"{endpoint}_{json.dumps(data, sort_keys=True)}"

    # Generate SHA256 hash
    cache_key = hashlib.sha256(
        cache_string.encode()
    ).hexdigest()

    return f"tool134:{endpoint}:{cache_key}"


def get_cached_response(cache_key):
    """
    Get cached response from Redis.
    Returns None if not found or Redis unavailable.
    """
    try:
        client = get_redis_client()
        if client is None:
            return None

        cached = client.get(cache_key)
        if cached:
            logger.info(f"Cache HIT: {cache_key[:30]}...")
            return json.loads(cached)

        logger.info(f"Cache MISS: {cache_key[:30]}...")
        return None

    except Exception as e:
        logger.warning(f"Cache get error: {str(e)}")
        return None


def set_cached_response(cache_key, data, ttl=900):
    """
    Save response to Redis cache.
    TTL = 900 seconds = 15 minutes
    After 15 minutes cache expires automatically.
    """
    try:
        client = get_redis_client()
        if client is None:
            return False

        client.setex(
            cache_key,
            ttl,
            json.dumps(data)
        )
        logger.info(f"Cache SET: {cache_key[:30]}... TTL={ttl}s")
        return True

    except Exception as e:
        logger.warning(f"Cache set error: {str(e)}")
        return False


def is_redis_connected():
    """
    Check if Redis is connected.
    Returns False quickly if not available.
    """
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            socket_connect_timeout=0.5,
            socket_timeout=0.5
        )
        r.ping()
        return True
    except Exception:
        return False