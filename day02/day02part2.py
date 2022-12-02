#answer = 11980

#filename = 'sample01.txt'
filename = 'input.txt'

score = 0
with open(filename, "r") as f:
    for line in f:
        #print(line)
        if line[2] == "X": #lose
            score += 0
            if line[0] == "A":
                score += 3
            elif line[0] == "B":
                score += 1
            elif line[0] == "C":
                score += 2
        elif line[2] == "Y": #draw
            score += 3
            if line[0] == "A":
                score += 1
            elif line[0] == "B":
                score += 2
            elif line[0] == "C":
                score += 3
        elif line[2] == "Z": #win
            score += 6
            if line[0] == "A":
                score += 2
            elif line[0] == "B":
                score += 3
            elif line[0] == "C":
                score += 1
print(score)

