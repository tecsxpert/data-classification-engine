# app.py — Entry point for Tool-134 AI Service
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# ─────────────────────────────────────────────
# REGISTER BLUEPRINTS
# ─────────────────────────────────────────────
# Blueprint = group of related endpoints
# We register describe_bp so /describe works
app.register_blueprint(describe_bp)


# ─────────────────────────────────────────────
# HEALTH CHECK ENDPOINT
# ─────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "Tool-134 AI Service",
        "version": "1.0.0",
        "port": os.getenv("FLASK_PORT", "5000")
    }), 200


# ─────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print("")
    print("  Tool-134 AI Service starting...")
    print(f"  Running on http://localhost:{port}")
    print(f"  Health check: http://localhost:{port}/health")
    print(f"  Describe:     http://localhost:{port}/describe")
    print("")
    app.run(host='0.0.0.0', port=port, debug=debug)