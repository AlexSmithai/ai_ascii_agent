import pyfiglet
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_ascii(text):
    """Generates ASCII art from text using pyfiglet."""
    fonts = ['slant', '3-d', '5lineoblique', 'big', 'block']
    font = random.choice(fonts)
    return pyfiglet.figlet_format(text, font=font)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if user_input.lower() == 'exit':
        return jsonify({"response": "Goodbye!"})
    response = f"Processing: {user_input}"
    ascii_response = generate_ascii(response)
    return jsonify({"response": ascii_response})

if __name__ == "__main__":
    app.run(debug=True)
