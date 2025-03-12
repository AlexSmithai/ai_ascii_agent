from flask import Flask, render_template, request, jsonify
from manus_agent import ManusAgent

app = Flask(__name__)
agent = ManusAgent(name="Manus", font="block", verbose=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    ascii_art = agent.get_ascii_art(text)
    return jsonify({'ascii_art': ascii_art})

if __name__ == '__main__':
    app.run(debug=True)
