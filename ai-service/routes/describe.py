# routes/describe.py
# This file handles POST /describe endpoint
# Java backend calls this when it needs AI description

from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import classify_data

# Blueprint is like a mini Flask app
# It groups related endpoints together
describe_bp = Blueprint('describe', __name__)


@describe_bp.route('/describe', methods=['POST'])
def describe():
    """
    POST /describe
    
    Receives dataset info and returns AI classification.
    
    Request body:
    {
        "dataset_name": "Customer_DB",
        "description": "Customer personal data",
        "fields": ["name", "email", "phone"]
    }
    
    Response:
    {
        "classification": "PII",
        "sensitivity_level": "HIGH",
        "description": "...",
        "generated_at": "2026-04-23T...",
        "is_fallback": false
    }
    """

    # ─────────────────────────────────────────
    # STEP 1 — GET REQUEST DATA
    # ─────────────────────────────────────────
    data = request.get_json()

    # Check if request body exists
    if not data:
        return jsonify({
            "error": "Request body is required",
            "status": 400
        }), 400

    # ─────────────────────────────────────────
    # STEP 2 — VALIDATE INPUT
    # ─────────────────────────────────────────

    # Check dataset_name exists
    if not data.get('dataset_name'):
        return jsonify({
            "error": "dataset_name is required",
            "status": 400
        }), 400

    # Check description exists
    if not data.get('description'):
        return jsonify({
            "error": "description is required",
            "status": 400
        }), 400

    # Check fields exists and is a list
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

    # Check fields is not empty
    if len(data.get('fields')) == 0:
        return jsonify({
            "error": "fields cannot be empty",
            "status": 400
        }), 400

    # ─────────────────────────────────────────
    # STEP 3 — SANITIZE INPUT
    # ─────────────────────────────────────────

    dataset_name = str(data['dataset_name']).strip()
    description = str(data['description']).strip()
    fields = [str(f).strip() for f in data['fields']]

    # Check for prompt injection attempts
    dangerous_phrases = [
        'ignore previous',
        'ignore above',
        'disregard',
        'forget instructions',
        'new instructions',
        'system prompt'
    ]

    combined_input = f"{dataset_name} {description}".lower()
    for phrase in dangerous_phrases:
        if phrase in combined_input:
            return jsonify({
                "error": "Invalid input detected",
                "status": 400
            }), 400

    # ─────────────────────────────────────────
    # STEP 4 — CALL AI SERVICE
    # ─────────────────────────────────────────
    result = classify_data(
        dataset_name=dataset_name,
        description=description,
        fields=fields
    )

    # ─────────────────────────────────────────
    # STEP 5 — ADD GENERATED AT TIMESTAMP
    # ─────────────────────────────────────────
    result['generated_at'] = datetime.utcnow().isoformat()

    # ─────────────────────────────────────────
    # STEP 6 — RETURN RESPONSE
    # ─────────────────────────────────────────
    return jsonify(result), 200