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

    with Image.open(filename) as img:
        # Convert the image to RGBA if it's not already to handle transparency
        img = img.convert('RGBA')
        data = np.array(img)
        # Check if the image is grayscale (only one channel)
        if len(data.shape) == 2 or (len(data.shape) == 3 and data.shape[2] == 1):
            # Return as a list of lists (each row is a list)
            return data.tolist()
        else:  # For RGB or RGBA images
            # Discard the alpha channel if present and return as list of lists of lists
            return data[:, :, :3].tolist()






def write_png(filename: str, content: list) -> None:
    # Assuming the first element's structure indicates the content's structure
    if isinstance(content[0][0], int):  # This suggests a grayscale image
        mode = 'L'
        height = len(content)
        array_content = np.array(content, dtype=np.uint8).reshape((height, -1))
    elif isinstance(content[0][0], list) and len(content[0][0]) == 3:  # RGB
        mode = 'RGB'
        array_content = np.array(content, dtype=np.uint8)
    else:
        raise ValueError("Unsupported image format.")

    image = Image.fromarray(array_content, mode=mode)
    image.save(filename, format='PNG')


if __name__ == "__main__":
    # Assuming the path "../s.png" is correct and accessible
    content = read_png("./s.png")
    # Assuming you want to save the output with a filename, adding ".png" to your provided "../F"
    write_png("./F.png", content)

