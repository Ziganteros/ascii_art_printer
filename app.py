from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os
from utils.art_generator import scikit_image_generator, gray_scale_image_generator


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ASCII_FOLDER = 'ascii_results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ASCII_FOLDER'] = ASCII_FOLDER

# Assicurati che le cartelle esistano
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ASCII_FOLDER, exist_ok=True)

# Variabile per memorizzare l'immagine corrente
current_image_path = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_image_path
    generator = None
    ascii_art = None
    # parametri per generatore in scala di grigi
    ascii_chars = '@%#*+=-:. '
    # parametri per generatore scikit
    edge_char = 'o'
    block_size = 4

    if request.method == 'POST':
        if 'image' in request.files:  # Upload immagine
            file = request.files['image']
            ascii_chars = request.form.get('ascii_chars', ascii_chars)
            edge_char = request.form.get('edge_char', edge_char)
            block_size = request.form.get('block_size', block_size)

            if file:
                # Salva l'immagine caricata
                current_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(current_image_path)

            if "ScalaDiGrigi" in request.form:
                # Genera ASCII art
                generator = 'ScalaDiGrigi'
                ascii_art = gray_scale_image_generator(current_image_path, ascii_chars)
            
            elif "Scikit" in request.form:
                # Genera ASCII art
                generator = 'Scikit'
                ascii_art = scikit_image_generator(current_image_path, edge_char, block_size)

        elif 'ascii_chars' in request.form:  # Modifica caratteri
            ascii_chars = request.form['ascii_chars']
            if current_image_path:
                generator = 'ScalaDiGrigi'
                ascii_art = gray_scale_image_generator(current_image_path, ascii_chars)

        elif 'edge_char' in request.form:  # Modifica caratteri
            edge_char = request.form['edge_char']
            block_size = request.form['block_size']
            if current_image_path:
                generator = 'Scikit'
                ascii_art = scikit_image_generator(current_image_path, edge_char, block_size)                

    return render_template(
        'index.html', 
        ascii_art=ascii_art, generator=generator,
        ascii_chars=ascii_chars,
        edge_char=edge_char, block_size=block_size)

@app.route('/download')
def download_file():
    """Permette di scaricare l'ASCII art generata come file .txt."""
    if current_image_path:
        ascii_file_path = os.path.join(app.config['ASCII_FOLDER'], "ascii_art.txt")
        if os.path.exists(ascii_file_path):
            return send_file(ascii_file_path, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
