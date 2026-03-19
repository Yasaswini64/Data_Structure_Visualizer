from flask import Flask, request, jsonify
import cohere
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 🔥 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 Get API key
api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    raise ValueError("❌ COHERE_API_KEY not found in environment variables")

co = cohere.Client(api_key)

# ✅ Home route (important for Render)
@app.route("/")
def home():
    return "Backend is running 🚀"

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response
# ✅ AI Route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json

        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        question = data["question"]

        response = co.chat(
            model="command-a-03-2025",
            message=f"""
You are a Data Structures and Algorithms expert.

For the given problem:
1. Identify the most suitable algorithm.
2. Provide time complexity.
3. Provide space complexity.
4. Give a short reason.

Return ONLY in this format:

Algorithm: <name>

Time Complexity: <time>

Space Complexity: <space>

Reason: <short reason>

Problem: {question}
"""
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 Run locally (Render uses gunicorn, so this is optional)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)