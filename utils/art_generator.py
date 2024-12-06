import numpy as np
from skimage import io, color
from skimage.feature import canny
from skimage.filters import gaussian
from skimage.transform import resize
from PIL import Image

def select_symbol(sub_array, edge_char):
    """
    Determina il simbolo da assegnare al quadratino.
    Ritorna 'o' se il blocco contiene bordi, altrimenti ' '.
    """
    # Calcola la densità del blocco
    density = np.sum(sub_array) / sub_array.size
    
    # Soglia per considerare il blocco non vuoto
    return edge_char if density > 0.1 else ' '*len(edge_char)

#def scikit_process_image(image_path, output_file, block_size=8):
def scikit_image_generator(image_path, edge_char, block_size):
    """
    Genera un file di testo contenente la rappresentazione ASCII dell'immagine.
    """
    # Carica e processa l'immagine
    image = io.imread(image_path)
    gray_image = color.rgb2gray(image)
    blurred_image = gaussian(gray_image, sigma=1)
    edges = canny(blurred_image, sigma=1)
    block_size = int(block_size)
    
    # Ridimensiona l'immagine per un migliore controllo sui dettagli
    height, width = edges.shape
    scaled_height = (height // block_size) * block_size
    scaled_width = (width // block_size) * block_size
    edges_resized = resize(edges, (scaled_height, scaled_width), anti_aliasing=False)
    
    # Suddivisione in blocchi e conversione in simboli
    ascii_art = []
    for y in range(0, scaled_height, block_size):
        row = []
        for x in range(0, scaled_width, block_size):
            block = edges_resized[y:y+block_size, x:x+block_size]
            row.append(select_symbol(block, edge_char))
        ascii_art.append("".join(row))
    
    return '\n'.join(ascii_art)



def gray_scale_image_generator(image_path='uploads/allegri.jpg', ascii_chars='@%#*+=-:. '):
    """Converte un'immagine in ASCII art."""
    scale_width = 100
    img = Image.open(image_path)

    # Ridimensiona e converte in scala di grigi
    aspect_ratio = img.height / img.width
    new_height = int(scale_width * aspect_ratio * 0.55)
    img = img.resize((scale_width, new_height)).convert('L')

    # Mappa dei caratteri
    pixels = img.getdata()
    ascii_str = "".join([ascii_chars[pixel // (256 // (len(ascii_chars)-1))] for pixel in pixels])
    
    # Spezza in righe
    ascii_lines = [ascii_str[i:i + scale_width] for i in range(0, len(ascii_str), scale_width)]
    return "\n".join(ascii_lines)
