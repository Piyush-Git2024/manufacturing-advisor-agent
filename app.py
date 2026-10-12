from flask import Flask, request, jsonify
from services.advisor_service import get_advisor_response

app = Flask(__name__)


@app.route("/health")
def health():
    return {
        "status": "UP",
        "service": "Manufacturing Advisor"
    }


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    question = data.get("question", "")

    response = get_advisor_response(question)

    return jsonify({
        "question": question,
        "response": response
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )