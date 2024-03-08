import sys
import pgm

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

if  __name__ == "__main__":
    filein = sys.argv[1]
    fileout = sys.argv[2]
    contentin = pgm.read_pgm(filein)
    contentout = hide_pattern_per_line(contentin, "PIERRE")
    print(contentout[0][0])
    pgm.write_pgm(fileout, contentout)