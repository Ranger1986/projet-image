"""Insertion d'un watermark dans une image"""
import math
import numpy as np

def hide_watermark(image: np.ndarray, watermark: str) -> np.ndarray:
    """Insère un watermark dans une image en modifiant les bits de poids faible

    Args:
        image (np.ndarray): Image à laquelle insérer le watermark
        watermark (str): Watermark à insérer dans l'image

    Returns:
        np.ndarray: Image avec le watermark inséré
    """
    watermark_bits = "".join(format(ord(char), '08b') for char in watermark)
    watermark_length = len(watermark_bits)
    watermark_iterator = 0
    image_with_watermark = image.copy()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                pixel = image[i, j, k]
                watermark_bit = int(watermark_bits[watermark_iterator])
                new_pixel = (pixel & 0b11111110) | watermark_bit
                image_with_watermark[i, j, k] = new_pixel
                watermark_iterator = (watermark_iterator + 1) % watermark_length

    return image_with_watermark

def psnr(original: np.ndarray, changed: np.ndarray) -> float:
    """Calcule le PSNR entre deux images

    Args:
        original (np.ndarray): Image originale
        changed (np.ndarray): Image modifiée

    Returns:
        float: Valeur du PSNR
    """
    mse = np.mean((original - changed) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr_value = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr_value

# Exemple d'utilisation
# from file_manipulation import read_image, write_image
# if __name__ == "__main__":
#     image_path = "../Image/blahaj.png"
#     output_path = "blahaj_hidden_pattern.png"
#     watermark = "WATERMARK"
    
#     image = read_image(image_path)
#     watermarked_image = hide_watermark(image, watermark)
#     print(psnr(image, watermarked_image))
#     write_image(watermarked_image, output_path)
