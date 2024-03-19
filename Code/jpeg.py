from PIL import Image

def read_jpeg(filename: str) -> list[list[int]]:
    """Reads a JPEG image and returns a list of lists representing the pixel values.

    Args:
        filename (str): The path to the JPEG image file.

    Returns:
        list[list[int]]: A list of lists representing the pixel values of the image.
    """

    try:
        with Image.open(filename) as image:
            width, height = image.size
            mode = image.mode  # Get image mode (e.g., 'RGB', 'L')
            content = []
            if mode == 'RGB':
                for y in range(height):
                    row = []
                    for x in range(width):
                        r, g, b = image.getpixel((x, y))
                        row.append(r)
                        row.append(g)
                        row.append(b)
                    content.append(row)
            elif mode == 'L':
                for y in range(height):
                    row = []
                    for x in range(width):
                        pixel_value = image.getpixel((x, y))
                        row.append(pixel_value)
                    content.append(row)
            else:
                raise NotImplementedError(f"Image mode {mode} not supported")
            

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    
    return content


def write_jpeg(filename: str, content: list[list[int]]) -> None:
    """Saves a list of lists representing pixel data as a JPEG image.

    Args:
        filename (str): The path to save the JPEG image.
        content (list[list[int]]): A list of lists containing pixel values.
              - For RGB images, each inner list should have three integers
                representing red, green, and blue intensities (0-255).
              - For grayscale images, each inner list should have one integer
                representing the grayscale intensity (0-255).
    """

    if len(content[0]) == 3:
        mode = 'RGB'
    else:
        mode = 'L'

    image = Image.fromarray(content, mode)
    image.save(filename, format='JPEG')

    
