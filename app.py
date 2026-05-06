from flask import Flask, Response, request, stream_with_context , render_template
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/chat"

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/chat', methods=['POST'])
def chat():

    data = request.get_json()
    messages = data.get('messages', [])

    def generate():
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "llama3",
                "messages": messages,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")

                try:
                    chunk = json.loads(decoded)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                except:
                    pass

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)