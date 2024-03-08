import sys
def read_pgm(nomFichier : str)->list[list[str]]:
    fichier = open(nomFichier,"rb")
    header = fichier.readline()
    assert header[:2] == b'P5'
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
                pixel_value = int(binary_num, 2)
                fichier.write(pixel_value.to_bytes(1, byteorder='big'))
        fichier.close()
    
def PSNR(content1 : list[list[str]], content2 : list[list[str]]):
    pass
def find_modification(content1 : list[list[str]], content2 : list[list[str]]):
    pass
        
if  __name__ == "__main__":
    filein = sys.argv[1]
    fileout = sys.argv[2]
    content = read_pgm(filein)
    
    write_pgm(fileout, content)