import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "Tool-134 AI Service",
        "version": "1.0.0",
        "port": os.getenv("FLASK_PORT", "5000")
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print("")
    print("  Tool-134 AI Service starting...")
    print(f"  Running on http://localhost:{port}")
    print(f"  Health check: http://localhost:{port}/health")
    print("")
    app.run(host='0.0.0.0', port=port, debug=debug)