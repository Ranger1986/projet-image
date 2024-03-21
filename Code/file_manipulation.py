"""Manipulation d'image a l'aide des bibliotheque pillow et numpy"""
from PIL import Image
import numpy as np


def read_image(file_path: str) -> np.ndarray:
    """Lis une image

    Args:
        file_path (str): Image a lire

    Returns:
        np.ndarray: tableau de pixel
    """
    img = Image.open(file_path)
    img_array = np.array(img)
    return img_array

def write_image(img_array: np.ndarray, output_path: str):
    """Ecris une image

    Args:
        img_array (np.ndarray): tableau de pixel
        output_path (str): Image a ecrire
    """
    img = Image.fromarray(img_array)
    img.save(output_path)
