import requests
import os
import ascii_magic
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Get Pexels API Key from Railway Environment Variables
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_image_from_web(search_query):
    """Fetches an image from Pexels API and ensures it is processable."""
    try:
        search_url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}

        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching image: {response.status_code} - {response.text}")
            return None

        image_results = response.json().get("photos", [])
        if not image_results:
            print("No images found for the search query.")
            return None

        # Get the first high-quality image
        image_url = image_results[0]["src"]["original"]
        print(f"Fetched Image URL: {image_url}")

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))
            image = image.convert("L")  # Convert to grayscale for better ASCII
            image = image.resize((60, 30))  # Resize to fit chatbox
            return image

    except Exception as e:
        print(f"Image fetching error: {str(e)}")
        return None

    return None

def generate_ascii_art(prompt):
    """Fetches an image and converts it into ASCII art."""
    try:
        image = fetch_image_from_web(prompt)
        if image:
            # Fix: Removed incorrect 'mode' argument
            ascii_art = ascii_magic.from_pillow_image(image)
            return ascii_art  # Correct output as a string
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
    return jsonify({"response": str(ascii_response)})  # Ensure it's converted to string

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
