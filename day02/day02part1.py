#answer = 12740

#filename = 'sample01.txt'
filename = 'input.txt'

score = 0
with open(filename, "r") as f:
    for line in f:
        #print(line)
        if line[2] == "X":
            score += 1
            if line[0] == "A":
                score += 3
            elif line[0] == "B":
                score += 0
            elif line[0] == "C":
                score += 6
        elif line[2] == "Y":
            score += 2
            if line[0] == "A":
                score += 6
            elif line[0] == "B":
                score += 3
            elif line[0] == "C":
                score += 0
        elif line[2] == "Z":
            score += 3
            if line[0] == "A":
                score += 0
            elif line[0] == "B":
                score += 6
            elif line[0] == "C":
                score += 3
print(score)

