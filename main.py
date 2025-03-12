from flask import Flask, render_template, request, jsonify
import requests
import ascii_magic
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "your-api-key-here")
PEXELS_URL = "https://api.pexels.com/v1/search"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_ascii')
def generate_ascii():
    query = request.args.get("query", "").strip()
    
    if not query:
        return jsonify({"success": False, "error": "Empty input"})

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    
    response = requests.get(PEXELS_URL, headers=headers, params=params)
    if response.status_code != 200 or not response.json().get("photos"):
        return jsonify({"success": False, "error": "No images found."})

    image_url = response.json()["photos"][0]["src"]["medium"]

    try:
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        ascii_art = ascii_magic.from_image(img, mode=ascii_magic.Modes
