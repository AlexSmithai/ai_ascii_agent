from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ASCII_FOLDER'] = 'ascii_art'

# Ensure upload and ASCII art directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ASCII_FOLDER'], exist_ok=True)

def image_to_ascii(image_path, output_path, width=100):
    """Converts an image to ASCII art and saves it as an image."""
    # Open the image
    image = Image.open(image_path)
    # Convert to grayscale
    gray_image = image.convert('L')
    # Resize image while maintaining aspect ratio
    aspect_ratio = gray_image.height / gray_image.width
    new_height = int(aspect_ratio * width * 0.55)
    resized_image = gray_image.resize((width, new_height))
    # Convert image to numpy array
    image_array = np.array(resized_image)
    # Define ASCII characters
    ascii_chars = "@%#*+=-:. "
    # Normalize pixel values to range from 0 to len(ascii_chars)
    normalized_pixels = (image_array - image_array.min()) / (image_array.max() - image_array.min())
    indices = (normalized_pixels * (len(ascii_chars) - 1)).astype(int)
    # Create ASCII art
    ascii_art = "\n".join("".join(ascii_chars[pixel] for pixel in row) for row in indices)
    # Save ASCII art to an image
    ascii_image = Image.new('L', (width * 6, new_height * 15), color=255)
    draw = ImageDraw.Draw(ascii_image)
    font = ImageFont.load_default()
    draw.text((0, 0), ascii_art, fill=0, font=font)
    ascii_image.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            ascii_filename = f'ascii_{filename.rsplit(".", 1)[0]}.png'
            ascii_path = os.path.join(app.config['ASCII_FOLDER'], ascii_filename)
            image_to_ascii(upload_path, ascii_path)
            return render_template('index.html', ascii_image=ascii_filename)
    return render_template('index.html', ascii_image=None)

@app.route('/ascii_art/<filename>')
def ascii_art(filename):
    return send_file(os.path.join(app.config['ASCII_FOLDER'], filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
