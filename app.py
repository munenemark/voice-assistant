import os
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini AI Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route("/api/command", methods=["POST"])
def process_voice_command():
    data = request.get_json()
    command = data.get("command", "").strip()
    command_lower = command.lower()
    
    response_text = ""

    # 1. HARDCODED SYSTEM COMMANDS
    if "time" in command_lower or "clock" in command_lower:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current time is {current_time}."
        
    elif "status" in command_lower:
        response_text = "Tobi's Python backend is online and powered by Gemini AI!"

    # 2. GENERAL QUESTIONS / CONVERSATIONS (Passed to Gemini AI)
    else:
        if not client:
            response_text = "Gemini API key is missing. Please check server setup."
        else:
            try:
                # Keep responses concise so Tobi speaks naturally
                prompt = f"You are Tobi, a helpful voice assistant. Keep your response brief, friendly, and under 3 sentences. User said: {command}"
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                response_text = response.text
            except Exception as e:
                error_str = str(e)
                print(f"❌ Gemini Error: {error_str}")  # Prints to your terminal / Render logs
                if "429" in error_str or "Quota" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    response_text = "I'm receiving requests too quickly! Please wait about 30 seconds before asking again."
                else:
                    response_text = "I ran into a temporary issue connecting to my AI brain."

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    print("🚀 Tobi Backend with Gemini AI is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)