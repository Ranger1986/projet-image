from PIL import Image
import numpy as np

def read_png(filename: str) -> None:
    """Reads a PNG image and returns its pixel data as a list of lists.

    Args:
        filename (str): The path to the PNG image file.

    Returns:
        list[list]: A list of lists containing pixel data. The structure
                   depends on the image mode (RGB, grayscale, etc.).
    """

    try:
        with Image.open(filename) as image:
            # Access pixel data based on image mode
            mode = image.mode
            if mode == 'RGB':
                content = [[r, g, b] for r, g, b in image.getdata()]
            elif mode == 'L':
                content = [[pixel] for pixel in image.getdata()]
            else:
                raise NotImplementedError(f"Image mode {mode} not supported")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")

    return content




def write_png(filename: str, content: list[list[int]]) -> None:
    """Saves pixel data as a PNG image.

    Args:
        filename (str): The path to save the PNG image.
        content (list[list[int]]): A list of lists containing pixel data.
            - For RGB images, each inner list should have three integers (0-255)
              representing red, green, and blue intensities.
            - For grayscale images, each inner list should have one integer (0-255)
              representing the grayscale intensity.

    Raises:
        ValueError: If the pixel data has incorrect dimensions or values.
    """

    if len(content[0]) != 3 and len(content[0]) != 1:
        raise ValueError("Image must be RGB (3 channels) or grayscale (1 channel).")

    height = len(content)
    width = len(content[0])
    mode = 'RGB' if len(content[0]) == 3 else 'L'
    image = Image.fromarray(np.asarray(content), mode)
    image.save(filename, format='PNG')
