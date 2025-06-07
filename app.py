from flask import Flask, request, jsonify, render_template
from gpt4all import GPT4All
import subprocess

app = Flask(__name__)

# Load the GPT-4-All model
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

def get_ai_response(prompt):
    """Generate AI response using GPT-4-All"""
    with model.chat_session():
        response = model.generate(prompt, max_tokens=1024)
    return response

def execute_script():
    """Run ExecScript.py"""
    print("Executing ExecScript.py...")  # Debugging log
    subprocess.run(["python", "ExecScript.py"])

@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is inside the 'templates' folder

@app.route("/process-prompt", methods=["POST"])
def process_prompt():
    data = request.json
    user_prompt = data.get("prompt")

    script_executed = False
    ai_response = get_ai_response(user_prompt)

    # **Override AI response if script is executed**
    if "execute script" in user_prompt.lower():
        execute_script()
        script_executed = True
        ai_response = "The script ExecScript.py has been successfully executed! ✅"

    return jsonify({"ai_response": ai_response, "script_executed": script_executed})

if __name__ == "__main__":
    app.run(debug=True)