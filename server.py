from flask import Flask, request, jsonify
import cohere
from flask_cors import CORS
import os
from dotenv import load_dotenv











# 🔥 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Get API key from .env (NOT hardcoded)
api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)
@app.route("/")
def home():
    return "Backend is running 🚀"


@app.route("/ask", methods=["POST"])

def ask():

    data = request.json
    print("Question received:", data)   # DEBUG

    question = data["question"]

    response = co.chat(
        model="command-a-03-2025",
        message=f"""
You are a Data Structures and Algorithms expert.

For the given problem:
1. Identify the most suitable algorithm to solve it.
2. Provide its time and space complexity.
3. Give a short reason.

Return ONLY in this format:

Algorithm: <algorithm name>

Time Complexity: <time complexity>

Space Complexity: <space complexity>

Reason: <one short sentence explaining why this algorithm is suitable>

Problem: {question}
"""
    )

    print("AI response:", response.text)   # DEBUG

    return jsonify({"answer": response.text})


if __name__ == "__main__":
    app.run(port=5000, debug=True)