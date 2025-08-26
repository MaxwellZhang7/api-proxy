from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GEN_API_KEY = os.environ.get("GEN_API_KEY")  # 在 Vercel 环境变量中设置

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
        "model": "gemini-2.5",
        "input": prompt
    }

    resp = requests.post("https://generativelanguage.googleapis.com/v1beta/models:generateText", 
                         headers=headers, json=payload)

    return jsonify(resp.json())
