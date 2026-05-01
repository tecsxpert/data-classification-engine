# routes/health.py
# Detailed health check endpoint
# Shows model, response time, uptime, cache status

from flask import Blueprint, jsonify
from datetime import datetime
from services.cache_service import is_redis_connected
import time
import os

health_bp = Blueprint('health', __name__)

# Track when service started
SERVICE_START_TIME = time.time()

# Track response times
response_times = []


def get_uptime():
    """
    Calculate how long service has been running.
    Returns formatted string like "2h 30m"
    """
    uptime_seconds = int(time.time() - SERVICE_START_TIME)

    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def get_avg_response_time():
    """
    Calculate average AI response time.
    Returns formatted string like "1.2s"
    """
    if not response_times:
        return "No requests yet"

    avg = sum(response_times) / len(response_times)
    return f"{avg:.2f}s"


def record_response_time(response_time):
    """
    Record a response time for averaging.
    Keeps only last 100 times.
    """
    response_times.append(response_time)
    # Keep only last 100 response times
    if len(response_times) > 100:
        response_times.pop(0)


@health_bp.route('/health', methods=['GET'])
def health():
    """
    GET /health

    Returns detailed health information:
    - status: ok/error
    - model: AI model being used
    - avg_response_time: average AI response time
    - uptime: how long service has been running
    - cache_status: Redis connection status
    - timestamp: current time
    """
    cache_connected = is_redis_connected()

    return jsonify({
        "status": "ok",
        "service": "Tool-134 AI Service",
        "version": "1.0.0",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time": get_avg_response_time(),
        "uptime": get_uptime(),
        "cache_status": "connected" if cache_connected else "unavailable",
        "port": os.getenv("FLASK_PORT", "5000"),
        "timestamp": datetime.utcnow().isoformat()
    }), 200