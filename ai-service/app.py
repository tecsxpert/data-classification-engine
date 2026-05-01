import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from routes.health import health_bp

load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)
app.register_blueprint(health_bp)


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "status": 404
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": "Method not allowed",
        "status": 405
    }), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "status": 500,
        "is_fallback": True
    }), 500


@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        "error": "Bad request",
        "status": 400
    }), 400


if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print("")
    print("  Tool-134 AI Service starting...")
    print(f"  Running on http://localhost:{port}")
    print(f"  Health:           http://localhost:{port}/health")
    print(f"  Describe:         http://localhost:{port}/describe")
    print(f"  Recommend:        http://localhost:{port}/recommend")
    print(f"  Generate Report:  http://localhost:{port}/generate-report")
    print("")
    app.run(host='0.0.0.0', port=port, debug=debug)