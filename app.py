from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/command", methods=["POST"])
def process_voice_command():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    response_text = ""

    # GREETINGS
    if "hello" in command or "hi" in command or "hey" in command:
        response_text = "Hello Mark! Tobi is online and ready to help."

    # TIME
    elif "time" in command or "clock" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current time is {current_time}."
    
    # JOKES
    elif "joke" in command:
        response_text = "Why do Python programmers prefer dark mode? Because light attracts bugs!"
        
    # STATUS
    elif "status" in command:
        response_text = "Tobi's Python backend is online and running smoothly!"
        
    else:
        response_text = f"Tobi's backend received: '{command}', but doesn't have a rule for it yet."

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    print("🚀 Tobi Backend is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)