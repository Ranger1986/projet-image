"""Trouve le watermark au sein d'une image"""

import numpy as np
def is_watermark_intact(image: np.ndarray, watermark: str) -> bool:
    """Vérifie si le watermark est intact dans l'image

    Args:
        image (np.ndarray): Image à vérifier
        watermark (str): Watermark à rechercher dans l'image

    Returns:
        bool: True si le watermark est intact, False sinon
    """
    watermark_bits = "".join(format(ord(char), '08b') for char in watermark)
    watermark_length = len(watermark_bits)
    watermark_iterator = 0

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                pixel = image[i, j, k]
                watermark_bit = int(watermark_bits[watermark_iterator])
                if (pixel & 0b00000001) != watermark_bit:
                    return False
                watermark_iterator = (watermark_iterator + 1) % watermark_length

    return True
def create_watermark_mask(image: np.ndarray, watermark: str) -> np.ndarray:
    """Crée un masque indiquant où le watermark est absent dans l'image

    Args:
        image (np.ndarray): Image à analyser
        watermark (str): Watermark à rechercher

    Returns:
        np.ndarray: Masque indiquant les zones sans watermark (blanches)
    """
    watermark_bits = "".join(format(ord(char), '08b') for char in watermark)
    watermark_length = len(watermark_bits)
    watermark_iterator = 0
    mask = np.zeros_like(image[:,:,0], dtype=np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                pixel = image[i, j, k]
                watermark_bit = int(watermark_bits[watermark_iterator])
                if (pixel & 0b00000001) != watermark_bit:
                    mask[i, j] = 255  # Blanc si le watermark est absent
                watermark_iterator = (watermark_iterator + 1) % watermark_length

    return mask
# Exemple d'utilisation
# from file_manipulation import read_image, write_image
# if __name__ == "__main__":
#     image_path = "blahaj_false.png"
#     watermark = "WATERMARK"
#     output_path = "false.png"
    
#     watermarked_image = read_image(image_path)
#     watermark_intact = is_watermark_intact(watermarked_image, watermark)
#     if watermark_intact:
#         print("Le watermark est intact dans l'image.")
#     else:
#         watermark_mask = create_watermark_mask(watermarked_image, watermark)
#         write_image(watermark_mask, output_path)
#         print("Le watermark a été altéré dans l'image.")