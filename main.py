import requests
from flask import Flask, render_template, request, jsonify
from art import text2art  # Generates ASCII art from text
import ascii_magic  # Generates ASCII images

app = Flask(__name__)

def generate_ascii_art(prompt):
    """Generates ASCII representation of an object using an external API or ASCII art library."""
    try:
        # Generate ASCII art from text-based representations (e.g., "horse")
        ascii_text = text2art(prompt, font="block")

        return ascii_text
    except Exception as e:
        return f"Error generating ASCII Art: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if user_input.lower() == 'exit':
        return jsonify({"response": "Goodbye!"})

    # Generate ASCII representation of the object
    ascii_response = generate_ascii_art(user_input)
    
    return jsonify({"response": ascii_response})

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
