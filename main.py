import pyfiglet
import random
import openai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# OpenAI API Key (Make sure to set it as an environment variable in Railway)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate AI-enhanced ASCII art
def generate_ai_ascii(prompt):
    """Uses OpenAI's latest API format to generate ASCII art."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Use the latest OpenAI model
            messages=[{"role": "system", "content": "You are an ASCII art generator."},
                      {"role": "user", "content": f"Generate ASCII art for: {prompt}"}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating AI ASCII: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if user_input.lower() == 'exit':
        return jsonify({"response": "Goodbye!"})
    
    # Generate AI-enhanced ASCII response
    ascii_response = generate_ai_ascii(user_input)
    return jsonify({"response": ascii_response})

if __name__ == "__main__":
    app.run(debug=True)
