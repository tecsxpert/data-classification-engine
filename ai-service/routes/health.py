# routes/health.py
from flask import Blueprint, jsonify
from datetime import datetime
import time
import os

health_bp = Blueprint('health', __name__)
SERVICE_START_TIME = time.time()


def get_uptime():
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


@health_bp.route('/health', methods=['GET'])
def health():
    """
    GET /health
    Returns instantly without Redis check
    """
    # Get average response time
    try:
        from services.groq_client import get_average_response_time
        avg_time = get_average_response_time()
    except Exception:
        avg_time = 0

    # Performance status
    if avg_time == 0:
        performance_status = "no requests yet"
    elif avg_time < 2.0:
        performance_status = "optimal"
    elif avg_time < 5.0:
        performance_status = "acceptable"
    else:
        performance_status = "slow"

    # Check Redis in background without blocking
    cache_status = "unavailable"
    try:
        import redis
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            socket_connect_timeout=0.3,
            socket_timeout=0.3
        )
        r.ping()
        cache_status = "connected"
    except Exception:
        cache_status = "unavailable"

    return jsonify({
        "status": "ok",
        "service": "Tool-134 AI Service",
        "version": "1.0.0",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time": f"{avg_time:.2f}s" if avg_time > 0 else "No requests yet",
        "performance_status": performance_status,
        "performance_target": "under 2.0s",
        "uptime": get_uptime(),
        "cache_status": cache_status,
        "port": os.getenv("FLASK_PORT", "5000"),
        "timestamp": datetime.utcnow().isoformat()
    }), 200