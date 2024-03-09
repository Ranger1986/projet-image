import sys
import pgm


def is_modified(content : list[list[str]], pattern: str)->bool:
    """Trouve si l'image a ete modifie

    Args:
        content (list[list[str]]): image en binaire
        pattern (str): texte caché dans l'image

    Returns:
        bool: si l'image a été modifiée
    """
    pattern_to_hide=""
    for char in pattern:
        pattern_to_hide+=bin(ord(char))[2:]
    length_of_pattern=len(pattern_to_hide)
    
    encodable_length= len(content[0]) - (len(content[0]) % length_of_pattern)
    for row in content:
        i=0
        for number in row[:encodable_length]:
            if number[-1]!=pattern_to_hide[i]:
                return True
            i+=1
            if i==length_of_pattern:
                i=0
    return False

def find_modification(content : list[list[str]], pattern: str)->list[list[str]]:
    """Trouve les parties modifiées de l'image

    Args:
        content (list[list[str]]): image en binaire
        pattern (str): texte caché dans l'image

    Returns:
        list[list[str]]: image de la trace des modifications en binaire
    """
    pattern_to_hide=""
    for char in pattern:
        pattern_to_hide+=bin(ord(char))[2:]
    length_of_pattern=len(pattern_to_hide)
    
    encodable_length= len(content[0]) - (len(content[0]) % length_of_pattern)
    contentout=[]
    for row in content:
        i=0
        rowout=[]
        for number in row[:encodable_length]:
            if number[-1]==pattern_to_hide[i]:
                rowout.append(bin(0)[2:])
            else:
                rowout.append(bin(255)[2:])
            i+=1
            if i==length_of_pattern:
                i=0
        # for number in row[encodable_length:]:
        #         rowout.append(bin(100)[2:])
        contentout.append(rowout)
    return contentout

if  __name__ == "__main__":
    assert len(sys.argv)==3, f"{sys.argv[0]} watermarkedFile.pgm falseTrace.pgm"
    file = sys.argv[1]
    fileout = sys.argv[2]
    content = pgm.read_pgm(file)
    contentout=find_modification(content, "PIERRE")
    pgm.write_pgm(fileout, contentout)