import sys
import pgm
import math
def hide_pattern_per_line(content : list[list[str]], pattern: str)->list[list[str]]:
    pattern_to_hide=""
    for char in pattern:
        pattern_to_hide+=bin(ord(char))[2:]
    length_of_pattern=len(pattern_to_hide)
    encodable_length= len(content[0]) - (len(content[0]) % length_of_pattern)
    contentout=[]#[[number for number in row] for row in content]
    for row in content:
        i=0
        rowout=[]
        for number in row[:encodable_length]:
            rowout.append(number[:-1]+pattern_to_hide[i])
            i+=1
            if i==length_of_pattern:
                i=0
        rowout+=row[encodable_length:]
        contentout.append(rowout)
    return contentout

def PSNR(original : list[list[str]], changed : list[list[str]])->float:
    EQM=0
    for i in range(len(original)):
        for j in range(len(original[i])):
            EQM+=pow(int(original[i][j],2)-int(changed[i][j],2),2)
    EQM/=len(original)*len(original[0])
    PSNR = 10 * math.log10(pow(255, 2) /EQM)
    return PSNR
    

if  __name__ == "__main__":
    assert len(sys.argv)==3, f"{sys.argv[0]} fileToWatermark.pgm watermarkedFile.pgm"
    filein = sys.argv[1]
    fileout = sys.argv[2]
    contentin = pgm.read_pgm(filein)
    contentout = hide_pattern_per_line(contentin, "PIERRE")
    print(PSNR(contentin,contentout))
    pgm.write_pgm(fileout, contentout)