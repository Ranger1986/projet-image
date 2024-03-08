def read_pgm(nomFichier : str)->list[list[str]]:
    fichier = open(nomFichier,"rb")
    header = fichier.readline()
    assert header[:2] == b'P5'
    secondline = fichier.readline()
    if chr(secondline[0])!='#':
        (width, height) = [int(i) for i in secondline.split()]
    else:
        (width, height) = [int(i) for i in fichier.readline().split()]
    depth = int(fichier.readline())
    assert depth <= 255
    content = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(bin(ord(fichier.read(1)))[2:])
        content.append(row)
    fichier.close
    return content

def write_pgm(nomFichier : str, content : list[list[str]])->None:
    #function corrected by chatGPT
    with open(nomFichier, "wb") as fichier:
        fichier.write(b'P5\n')
        dimensions = f"{len(content[0])} {len(content)}\n"
        fichier.write(dimensions.encode('utf-8'))
        fichier.write(b'255\n')
        for row in content:
            for binary_num in row:
                pixel_value = 0 if binary_num==0 else int(binary_num, 2)
                fichier.write(pixel_value.to_bytes(1, byteorder='big'))
        fichier.close()