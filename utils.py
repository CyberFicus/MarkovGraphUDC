from config import SHOW_PARSED_WORDS

def parse_file(fname: str):
    codewords = []
    file = open(fname, "r")

    for line in file:
        if "*" in line:
            print("Error, please remove \"*\" from input")
            exit()
        word = line.split()[0]

        if line == "":
            continue

        codewords.append(word)
    
    codewords.sort(key=len)
    
    if SHOW_PARSED_WORDS:
        print("Parsed codewords are:\n{", end="")
        i = 0
        for word in codewords:
            if i > 0:
                print(", ", end="")
            print(word, end="")
            i+=1
        print("}")
    
    return codewords

