# routes/report.py
# Handles POST /generate-report endpoint
# Returns full structured report

from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import generate_report

report_bp = Blueprint('report', __name__)


@report_bp.route('/generate-report', methods=['POST'])
def create_report():
    """
    POST /generate-report

    Request body:
    {
        "dataset_name": "Customer_DB",
        "classification": "PII",
        "sensitivity_level": "HIGH",
        "description": "Customer personal data",
        "fields": ["name", "email", "phone"]
    }

    Response:
    {
        "title": "Data Classification Report — Customer_DB",
        "summary": "...",
        "overview": "...",
        "key_items": [...],
        "recommendations": [...],
        "generated_at": "2026-05-01T...",
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
    required_fields = [
        'dataset_name',
        'classification',
        'sensitivity_level',
        'description',
        'fields'
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"{field} is required",
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

    # ─────────────────────────────────────────
    # STEP 3 — SANITIZE INPUT
    # ─────────────────────────────────────────
    dataset_name = str(data['dataset_name']).strip()
    classification = str(data['classification']).strip()
    sensitivity_level = str(data['sensitivity_level']).strip()
    description = str(data['description']).strip()
    fields = [str(f).strip() for f in data['fields']]

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
    result = generate_report(
        dataset_name=dataset_name,
        classification=classification,
        sensitivity_level=sensitivity_level,
        description=description,
        fields=fields
    )

    # ─────────────────────────────────────────
    # STEP 5 — ADD TIMESTAMP
    # ─────────────────────────────────────────
    result['generated_at'] = datetime.utcnow().isoformat()

    # ─────────────────────────────────────────
    # STEP 6 — RETURN RESPONSE
    # ─────────────────────────────────────────
    return jsonify(result), 200