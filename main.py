import os
import requests
import ascii_magic
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify, render_template

# Flask app initialization
app = Flask(__name__)

# Pexels API Key (Make sure it's set in your Railway environment variables)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_image_from_web(query):
    """Fetch an image from Pexels API based on the search query."""
    if not PEXELS_API_KEY:
        return None  # API key is missing

    try:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "photos" in data and len(data["photos"]) > 0:
                image_url = data["photos"][0]["src"]["medium"]
                image_response = requests.get(image_url)
                return Image.open(BytesIO(image_response.content))
        return None  # No images found
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def generate_ascii_art(prompt):
    """Generate ASCII art from an image search."""
    try:
        image = fetch_image_from_web(prompt)
        if image:
            # Generate ASCII art **without color**
            ascii_art = ascii_magic.from_pillow_image(image, mode=ascii_magic.Modes.ASCII).to_ascii()

            # Strip out any unwanted ANSI codes (color artifacts)
            ascii_art = ascii_art.replace("\033[34m", "").replace("\033[37m", "").replace("\033[0m", "")

            # Format properly for chatbox display
            return f"```\n{ascii_art}\n```"
        return "Error: Could not fetch an image for this object."
    except Exception as e:
        return f"Error generating ASCII Art: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Please enter an object to generate ASCII art for."})

    ascii_art = generate_ascii_art(prompt)
    return jsonify({"ascii_art": ascii_art})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
