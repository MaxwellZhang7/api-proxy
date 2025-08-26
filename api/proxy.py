from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GEN_API_KEY = os.environ.get("GEN_API_KEY")
if not GEN_API_KEY:
    raise ValueError("GEN_API_KEY environment variable is not set")

MODEL_NAME = "gemini-2.5"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateText"

@app.route("/api/proxy", methods=["POST"])
def proxy():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    headers = {
        "Authorization": f"Bearer {GEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": [{"content": prompt, "type": "text"}]
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), 
                        "status_code": resp.status_code if 'resp' in locals() else None}), 500
