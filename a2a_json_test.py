from flask import Flask, jsonify, request

app = Flask(__name__)

NGROK_URL = "https://enjoyer-jellied-gloss.ngrok-free.dev"


# ==========================================================
# Agent Card
# ==========================================================
@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():

    return jsonify({
        "protocolVersion": "0.3.0",

        "name": "JSON Test Agent",

        "description":
        "Agent used to test application/json support in Pega",

        "url": NGROK_URL,

        "version": "1.0.0",

        "capabilities": {
            "streaming": False
        },

        "skills": [
            {
                "id": "json-test",

                "name": "JSON Test",

                "description":
                "Returns JSON payload",

                "inputModes": [
                    "application/json"
                ],

                "outputModes": [
                    "application/json"
                ]
            }
        ]
    })


# ==========================================================
# A2A Endpoint
# ==========================================================
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return "JSON Test Agent Running"

    payload = request.get_json(silent=True) or {}

    print("\n=================================")
    print("REQUEST RECEIVED")
    print(payload)
    print("=================================\n")

    response = {
        "jsonrpc": "2.0",

        "id": payload.get("id", "1"),

        "result": {

            "id": "json-test-001",

            "kind": "task",

            "status": {
                "state": "completed"
            },

            "artifacts": [
                {
                    "name": "json-test",

                    "index": 0,

                    "parts": [
                        {
                            "kind": "data",

                            "type": "application/json",

                            "data": {
                                "machine": "CNC101",
                                "riskLevel": "HIGH",
                                "temperature": 92,
                                "recommendation":
                                "Immediate maintenance required"
                            }
                        }
                    ]
                }
            ]
        }
    }

    return jsonify(response)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )