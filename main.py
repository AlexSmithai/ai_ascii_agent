import os
import flask
import ascii_magic
from flask import Flask, request, jsonify, render_template
from art import text2art
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

# Load Pexels API key from environment variables
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def generate_ascii_art_from_text(text):
    try:
        return text2art(text)
    except Exception as e:
        return f"Error generating ASCII Art: {e}"

def generate_ascii_art_from_image(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        ascii_art = ascii_magic.from_image(image)
        return ascii_art
    except Exception as e:
        return f"Error processing image: {e}"

def search_image(query):
    """ Fetch an image from Pexels API """
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["original"]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_ascii():
    data = request.json
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({"error": "Input cannot be empty"}), 400

    # Check if the input is an image request
    image_url = search_image(user_input)
    
    if image_url:
        ascii_art = generate_ascii_art_from_image(image_url)
    else:
        ascii_art = generate_ascii_art_from_text(user_input)

    return jsonify({"ascii_art": ascii_art})

if __name__ == "__main__":
    app.run(debug=True)

