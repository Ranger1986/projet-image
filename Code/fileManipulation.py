from PIL import Image
import numpy as np

def read_image(file_path):
    # Ouvrir l'image avec Pillow
    img = Image.open(file_path)
    # Convertir l'image en tableau NumPy
    img_array = np.array(img)
    return img_array

def write_image(img_array, output_path):
    # Convertir le tableau NumPy en image avec Pillow
    img = Image.fromarray(img_array)
    # Enregistrer l'image
    img.save(output_path)

# Exemple d'utilisation
if __name__ == "__main__":
    # Chemin vers l'image d'entrée
    input_image_path = "input.png"
    # Chemin pour enregistrer l'image de sortie
    output_image_path = "output.jpg"

    # Lire l'image
    image_array = read_image(input_image_path)
    modified_image_array = image_array
    
    # Modifier l'image

    # Enregistrer l'image modifiée
    write_image(modified_image_array, output_image_path)
