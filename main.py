import requests
import ascii_magic  # Generates ASCII art
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_ascii_art(image_path):
    """Generates ASCII art from an image."""
    try:
        # Generate ASCII art without using 'columns' since from_image() does not support it
        ascii_art = ascii_magic.from_image(image_path)
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

    # Assuming an image mapping based on user input (e.g., "horse" -> "horse.jpg")
    image_path = f"static/images/{user_input.lower()}.jpg"  # Adjust path based on available images
    ascii_response = generate_ascii_art(image_path)
    
    return jsonify({"response": ascii_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
