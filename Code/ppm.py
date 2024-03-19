def read_ppm(nomFichier: str) -> list[list[tuple]]:
    """Reads a PPM image file and returns its pixel data as a list of RGB tuples.

    Args:
        nomFichier (str): The path to the PPM image file.

    Returns:
        list[list[tuple]]: A list of lists containing RGB tuples (red, green, blue).

    Raises:
        ValueError: If the file format is not PPM, or if the header information is invalid.
        FileNotFoundError: If the specified file cannot be found.
    """

    with open(nomFichier, "rb") as fichier:
        header = fichier.readline().decode('utf-8').strip()
        if header[:2] != 'P6':
            raise ValueError(f"Invalid image format: {header}")

        # Extract dimensions (specific to PPM)
        secondline = fichier.readline().decode('utf-8').strip()
        try:
            (width, height) = [int(i) for i in secondline.split()]
            if width <= 0 or height <= 0:
                raise ValueError("Invalid image dimensions")
        except ValueError:
            raise ValueError("Invalid width or height in header")

        # Read maximum color value (specific to PPM)
        depth_line = fichier.readline().decode('utf-8').strip()
        try:
            depth = int(depth_line)
            if depth <= 0 or depth > 255:
                raise ValueError("Invalid maximum color value")
        except ValueError:
            raise ValueError("Invalid maximum color value in header")

        content = []
        for i in range(height):
            row = []
            for j in range(width):
                # Read three bytes for RGB values
                red = int.from_bytes(fichier.read(1), "big")
                green = int.from_bytes(fichier.read(1), "big")
                blue = int.from_bytes(fichier.read(1), "big")
                row.append((red, green, blue))
            content.append(row)

    return content


def write_ppm(nomFichier: str, content: list[list[tuple]]) -> None:
    """Exports a PPM image.

    Args:
        nomFichier (str): The path to save the PPM image.
        content (list[list[tuple]]): A list of lists containing RGB tuples (red, green, blue).
    """

    with open(nomFichier, "wb") as fichier:
        fichier.write(b'P6\n')  # PPM header
        dimensions = f"{len(content[0])} {len(content)}\n"
        fichier.write(dimensions.encode('utf-8'))
        fichier.write(b'255\n')  # Maximum color value

        for row in content:
            for pixel in row:
                red, green, blue = pixel
                fichier.write(red.to_bytes(1, byteorder='big'))
                fichier.write(green.to_bytes(1, byteorder='big'))
                fichier.write(blue.to_bytes(1, byteorder='big'))
