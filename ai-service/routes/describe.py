# routes/describe.py
# Handles POST /describe endpoint
# Now with Redis caching!

from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import classify_data
from services.cache_service import (
    generate_cache_key,
    get_cached_response,
    set_cached_response
)
import time

describe_bp = Blueprint('describe', __name__)


@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required",
            "status": 400
        }), 400

    if not data.get('dataset_name'):
        return jsonify({
            "error": "dataset_name is required",
            "status": 400
        }), 400

    if not data.get('description'):
        return jsonify({
            "error": "description is required",
            "status": 400
        }), 400

    if not data.get('fields'):
        return jsonify({
            "error": "fields is required",
            "status": 400
        }), 400

    if not isinstance(data.get('fields'), list):
        return jsonify({
            "error": "fields must be a list",
            "status": 400
        }), 400

    if len(data.get('fields')) == 0:
        return jsonify({
            "error": "fields cannot be empty",
            "status": 400
        }), 400

    # Sanitize
    dataset_name = str(data['dataset_name']).strip()
    description = str(data['description']).strip()
    fields = [str(f).strip() for f in data['fields']]

    # Check prompt injection
    dangerous_phrases = [
        'ignore previous', 'ignore above',
        'disregard', 'forget instructions',
        'new instructions', 'system prompt'
    ]
    combined_input = f"{dataset_name} {description}".lower()
    for phrase in dangerous_phrases:
        if phrase in combined_input:
            return jsonify({
                "error": "Invalid input detected",
                "status": 400
            }), 400

    # ─────────────────────────────────────────
    # CHECK CACHE FIRST
    # ─────────────────────────────────────────
    cache_key = generate_cache_key('describe', {
        'dataset_name': dataset_name,
        'description': description,
        'fields': fields
    })

    cached = get_cached_response(cache_key)
    if cached:
        cached['from_cache'] = True
        return jsonify(cached), 200

    # ─────────────────────────────────────────
    # CALL AI SERVICE
    # ─────────────────────────────────────────
    start_time = time.time()

    result = classify_data(
        dataset_name=dataset_name,
        description=description,
        fields=fields
    )

    # Record response time
    response_time = time.time() - start_time
    try:
        from routes.health import record_response_time
        record_response_time(response_time)
    except Exception:
        pass

    result['generated_at'] = datetime.utcnow().isoformat()
    result['from_cache'] = False

    # ─────────────────────────────────────────
    # SAVE TO CACHE
    # ─────────────────────────────────────────
    set_cached_response(cache_key, result, ttl=900)

    return jsonify(result), 200