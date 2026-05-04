# routes/recommend.py
# Handles POST /recommend endpoint
# Returns 3 actionable recommendations

from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import recommend_actions

recommend_bp = Blueprint('recommend', __name__)


@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    POST /recommend

    Request body:
    {
        "dataset_name": "Customer_DB",
        "classification": "PII",
        "sensitivity_level": "HIGH",
        "description": "Customer personal data"
    }

    Response:
    {
        "recommendations": [
            {
                "action_type": "ENCRYPT",
                "description": "...",
                "priority": "HIGH"
            },
            ...
        ],
        "generated_at": "2026-04-30T...",
        "is_fallback": false
    }
    """

    # ─────────────────────────────────────────
    # STEP 1 — GET REQUEST DATA
    # ─────────────────────────────────────────
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required",
            "status": 400
        }), 400

    # ─────────────────────────────────────────
    # STEP 2 — VALIDATE INPUT
    # ─────────────────────────────────────────
    if not data.get('dataset_name'):
        return jsonify({
            "error": "dataset_name is required",
            "status": 400
        }), 400

    if not data.get('classification'):
        return jsonify({
            "error": "classification is required",
            "status": 400
        }), 400

    if not data.get('sensitivity_level'):
        return jsonify({
            "error": "sensitivity_level is required",
            "status": 400
        }), 400

    if not data.get('description'):
        return jsonify({
            "error": "description is required",
            "status": 400
        }), 400

    # ─────────────────────────────────────────
    # STEP 3 — SANITIZE INPUT
    # ─────────────────────────────────────────
    dataset_name = str(data['dataset_name']).strip()
    classification = str(data['classification']).strip()
    sensitivity_level = str(data['sensitivity_level']).strip()
    description = str(data['description']).strip()

    # Check for prompt injection
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
    result = recommend_actions(
        dataset_name=dataset_name,
        classification=classification,
        sensitivity_level=sensitivity_level,
        description=description
    )

    # ─────────────────────────────────────────
    # STEP 5 — ADD TIMESTAMP
    # ─────────────────────────────────────────
    result['generated_at'] = datetime.utcnow().isoformat()

    # ─────────────────────────────────────────
    # STEP 6 — RETURN RESPONSE
    # ─────────────────────────────────────────
    return jsonify(result), 200