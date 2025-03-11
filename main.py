import requests
import ascii_magic
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def fetch_image_from_web(search_query):
    try:
        search_url = f"https://source.unsplash.com/400x400/?{search_query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Image fetching error: {str(e)}")
        return None
    return None

def generate_ascii_art(prompt):
    try:
        image = fetch_image_from_web(prompt)
        if image:
            ascii_art = ascii_magic.from_pillow_image(image)
            return str(ascii_art)
        return "Error: Unable to fetch an image for the given prompt."
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
