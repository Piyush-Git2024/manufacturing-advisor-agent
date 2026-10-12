from flask import Flask, jsonify, request

from services.advisor_service import get_advisor_response

app = Flask(__name__)

NGROK_URL = "https://enjoyer-jellied-gloss.ngrok-free.dev"


# ==========================================================
# Health Endpoint
# ==========================================================
@app.route("/health")
def health():

    return {
        "service": "Manufacturing Advisor A2A",
        "status": "UP"
    }


# ==========================================================
# Agent Card
# ==========================================================
@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():

    card = {
        "protocolVersion": "0.3.0",

        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },

        "description":
        "Provides manufacturing production, quality, maintenance and operational risk assessment",

        "name":
        "Manufacturing Advisor Agent",

        "skills": [
            {
                "description":
                "Production, quality, maintenance and risk analysis",

                "id":
                "manufacturing-analysis",

                "inputModes": [
                    "text/plain"
                ],

                "name":
                "Manufacturing Analysis",

                "outputModes": [
                    "text/plain"
                ],

                "tags": []
            }
        ],

        "url": NGROK_URL,

        "version": "1.0.0"
    }

    return jsonify(card)


# ==========================================================
# A2A Endpoint
# ==========================================================
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return "Manufacturing Advisor Agent Running"

    payload = request.get_json(silent=True) or {}

    request_id = payload.get("id", "1")

    params = payload.get("params", {})
    message = params.get("message", {})

    task_id = (
        params.get("id")
        or message.get("messageId")
        or "manufacturing-task-001"
    )

    question = ""

    try:
        question = message["parts"][0]["text"]
    except Exception:
        question = "help"

    print("\n===================================")
    print("QUESTION RECEIVED")
    print(question)
    print("===================================\n")

    answer = get_advisor_response(question)

    response = {
        "jsonrpc": "2.0",

        "id": request_id,

        "result": {
            "id": task_id,

            "kind": "task",

            "status": {
                "state": "completed"
            },

            "artifacts": [
                {
                    "name": "manufacturing-analysis",

                    "index": 0,

                    "parts": [
                        {
                            "kind": "text",

                            "type": "text",

                            "text": answer
                        }
                    ]
                }
            ]
        }
    }

    print("\nRESPONSE SENT")
    print(answer)
    print()

    return jsonify(response)


# ==========================================================
# Start Application
# ==========================================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )