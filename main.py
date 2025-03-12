import pyfiglet
import random
import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# OpenAI API Key (Replace with a secure method for production)
OPENAI_API_KEY = "your-api-key-here"

# Function to generate AI-enhanced ASCII art
def generate_ai_ascii(prompt):
    """Uses OpenAI's API to generate ASCII art from a prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Adjust to the latest OpenAI model
            messages=[{"role": "user", "content": f"Generate ASCII art for: {prompt}"}],
            max_tokens=300
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
