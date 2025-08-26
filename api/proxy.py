import json
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)

# 配置 Gemini 2.5 API Key
genai.configure(api_key="AIzaSyA7UCf2pgHX8dMlqDqxbbkRNweUSmfy9B8")

@app.route("/proxy", methods=["POST"])
def proxy():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return json.dumps({"error": "No prompt provided"}), 400

        response = genai.generate_text(
            model="gemini-2.5",
            prompt=prompt
        )
        return json.dumps({"text": response.text})
    except Exception as e:
        return json.dumps({"error": str(e)}), 500
