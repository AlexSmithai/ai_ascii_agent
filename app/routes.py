from flask import Blueprint, render_template, request, jsonify
from ai_agent.ascii_generator import generate_ascii_art

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "Manus AI")
    ascii_art = generate_ascii_art(text)
    return jsonify({"ascii_art": ascii_art})

@main.route("/about")
def about():
    return render_template("about.html")
