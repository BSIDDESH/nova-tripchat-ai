from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
from nova_client import chat_nova, plan_trip, find_hotels, estimate_budget, packing_list

load_dotenv()

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
CORS(app)

# Store conversation history per session
conversations = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        session_id = data.get("session_id", str(uuid.uuid4()))

        history = conversations.get(session_id, [])
        response, updated_history = chat_nova(user_message, history)
        conversations[session_id] = updated_history[-20:]

        return jsonify({
            "response": response,
            "session_id": session_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/plan-trip", methods=["POST"])
def plan_trip_route():
    try:
        data = request.json
        destination = data.get("destination", "")
        days = data.get("days", 5)
        budget = data.get("budget", 1000)

        response, _ = plan_trip(destination, days, budget)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/hotels", methods=["POST"])
def hotels_route():
    try:
        data = request.json
        destination = data.get("destination", "")
        budget_level = data.get("budget_level", "mid-range")

        response, _ = find_hotels(destination, budget_level)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/budget", methods=["POST"])
def budget_route():
    try:
        data = request.json
        destination = data.get("destination", "")
        days = data.get("days", 5)
        total_budget = data.get("total_budget", 1000)

        response, _ = estimate_budget(destination, days, total_budget)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/packing-list", methods=["POST"])
def packing_route():
    try:
        data = request.json
        destination = data.get("destination", "")
        days = data.get("days", 5)
        trip_type = data.get("trip_type", "general")

        response, _ = packing_list(destination, days, trip_type)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)