from flask import Flask, render_template, request, jsonify
from echo_agent import EchoAgent

app = Flask(__name__)

# Initialize ASCII AI Agent
ai_agent = EchoAgent(name="MANUS AI")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_ascii():
    data = request.json
    text = data.get("text", "MANUS AI")
    
    # Generate ASCII Art
    ascii_art = ai_agent.generate_ascii(text)
    
    return jsonify({"ascii": ascii_art})

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
