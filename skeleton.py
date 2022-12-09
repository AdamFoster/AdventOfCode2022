#answer = 

filename = 'sample01.txt'
#filename = 'input.txt'

data = []
with open(filename, "r") as f:
    for line in f:
        data.append(line.strip())

