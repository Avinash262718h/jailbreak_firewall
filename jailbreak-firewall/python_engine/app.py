from flask import Flask, request, jsonify
from flask_cors import CORS
from model_loader import SecurityEngine
import time
import logging

# Initialize Flask
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API_SERVER")

# --- GLOBAL ENGINE INITIALIZATION ---
# We load the model HERE, outside the request loop.
# This ensures we don't reload the model for every user (which would be slow).
try:
    engine = SecurityEngine()
    logger.info("🚀 AI Engine is warm and ready!")
except Exception as e:
    logger.critical(f"🔥 FATAL: Could not start AI Engine: {e}")
    engine = None

@app.route('/analyze', methods=['POST'])
def analyze_prompt():
    start_time = time.time()
    
    # 1. Validation
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.json
    user_prompt = data.get("prompt", "").strip()
    
    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    logger.info(f"📩 Processing Prompt: '{user_prompt[:50]}...'")

    # 2. Execution
    try:
        if engine is None:
            raise Exception("AI Engine is offline")

        # Call the logic from model_loader.py
        result = engine.analyze(user_prompt)
        
        # Add processing time for metrics
        process_time = round(time.time() - start_time, 3)
        result["processing_time_seconds"] = process_time
        
        logger.info(f"✅ Analysis Done. Verdict: {result['verdict']} (Time: {process_time}s)")
        
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"❌ Error analyzing prompt: {str(e)}")
        return jsonify({
            "verdict": "ERROR", 
            "recommendation": "System Error", 
            "details": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple endpoint to check if python is running"""
    status = "UP" if engine else "DOWN"
    return jsonify({"status": status, "model": "all-MiniLM-L6-v2"}), 200

if __name__ == '__main__':
    # Threaded=True handles multiple requests better
    print("⚡ Starting Jailbreak Firewall Python Backend on Port 5000...")
    app.run(port=5000, debug=True, threaded=True)