from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/chat"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    messages = data.get("messages", [])

    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": "llama3",
            "messages": messages,
            "stream": False
        }
    )

    result = response.json()

    print(result)

    return jsonify({
        "reply": result["message"]["content"]
    })

if __name__ == "__main__":
    app.run(debug=True)