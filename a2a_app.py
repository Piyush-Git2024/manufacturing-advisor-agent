from flask import Flask, jsonify, request

from services.advisor_service import get_advisor_response

app = Flask(__name__)

@app.route("/health")
def health():

    return {
        "service": "Manufacturing Advisor A2A",
        "status": "UP"
    }
@app.route("/.well-known/agent.json")
def agent_card():

    card = {
        "name": "Manufacturing Advisor Agent",
        "description": "AI agent that analyzes production, quality, maintenance and operational risks.",
        "url": "",
        "version": "1.0.0",

        "protocolVersion": "0.3.0",

        "capabilities": {
            "streaming": False
        },

        "defaultInputModes": [
            "text"
        ],

        "defaultOutputModes": [
            "text"
        ],

        "skills": [
            {
                "id": "manufacturing-analysis",
                "name": "Manufacturing Analysis",
                "description":
                "Production, quality, maintenance and risk analysis."
            }
        ]
    }

    return jsonify(card)
@app.route("/", methods=["POST"])
def handle_message():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    try:
        question = (
            data["params"]
                ["message"]
                ["parts"][0]
                ["text"]
        )

    except Exception:
        question = "help"

    answer = get_advisor_response(question)

    response = {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "kind": "task",
            "status": {
                "state": "completed"
            },
            "artifacts": [
                {
                    "parts": [
                        {
                            "kind": "text",
                            "text": answer
                        }
                    ]
                }
            ]
        }
    }

    print("Question:", question)
    print("Answer:", answer)

    return jsonify(response)

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )