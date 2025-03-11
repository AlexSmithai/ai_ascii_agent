import requests
import ascii_magic  # Generates ASCII art
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_ascii_art(prompt):
    """Generates ASCII art using an image-based approach."""
    try:
        # Use `from_image()` instead of `from_text()`
        ascii_art = ascii_magic.from_image("sample.jpg", columns=100)
        return str(ascii_art)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
