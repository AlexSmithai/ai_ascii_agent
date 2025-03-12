import requests
import os
import ascii_magic
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_image_from_web(search_query):
    """Fetch an image from Pexels API and return a processed Pillow Image."""
    try:
        search_url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}

        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return None

        image_results = response.json().get("photos", [])
        if not image_results:
            return None

        image_url = image_results[0]["src"]["original"]
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.convert("L")  # Convert to grayscale
            image = image.resize((50, 25))  # Resize for better chatbox fit
            return image

    except Exception:
        return None

    return None

def generate_ascii_art(prompt):
    """Generate ASCII art from an image search."""
    try:
        image = fetch_image_from_web(prompt)
        if image:
            ascii_art = ascii_magic.from_pillow_image(image).to_ascii()
            ascii_art = ascii_art.replace("\033[34m", "").replace("\033[0m", "")  # Remove ANSI color codes
            return f"```\n{ascii_art}\n```"  # Format it properly for chatbox
        return "Error: Could not fetch an image for this object."
    except Exception as e:
        return f"Error generating ASCII Art: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").lower()
    ascii_response = generate_ascii_art(user_input)
    return jsonify({"response": ascii_response})  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
