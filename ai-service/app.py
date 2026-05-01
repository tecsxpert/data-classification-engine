import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from routes.health import health_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)

# Fix proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app)

# ─────────────────────────────────────────────
# RATE LIMITING
# ─────────────────────────────────────────────
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)
app.register_blueprint(health_bp)


# ─────────────────────────────────────────────
# SECURITY HEADERS
# ─────────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


# ─────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────
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