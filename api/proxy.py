import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 读取环境变量中的 API Key
GENIE_API_KEY = os.environ.get("GENIE_API_KEY")
genai.configure(api_key=GENIE_API_KEY)

@app.route("/api/proxy", methods=["POST"])
def proxy():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    try:
        response = genai.chat.completions.create(
            model="gemini-2.5",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({
            "text": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
