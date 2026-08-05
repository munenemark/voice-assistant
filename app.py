from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Enables local cross-origin requests from your frontend

@app.route("/api/command", methods=["POST"])
def process_voice_command():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    response_text = ""

    # Backend Logic Handling
    if "time" in command or "clock" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current time is {current_time}."
    
    elif "joke" in command:
        response_text = "Why do Python programmers prefer dark mode? Because light attracts bugs!"
        
    elif "status" in command:
        response_text = "Tobi's Python backend is online and running smoothly!"
        
    else:
        # Fallback response for unhandled backend commands
        response_text = f"Tobi's backend received: '{command}', but doesn't have a rule for it yet."

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    print("🚀 Tobi Backend is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)