#answer = 69883

#filename = 'sample01.txt'
filename = 'input.txt'

elves = []


elf = {"total": 0, "foods": []}

def printelf(e):
    print(e["total"])

with open(filename, "r") as f:
    for line in f:
        #print(line)
        if line == "\n":
            elves.append(elf)
            #printelf(elf)
            elf = {"total": 0, "foods": []}
        else:
            lineasint = int(line)
            elf["total"] += lineasint
            elf["foods"].append(lineasint)

max = 0
for e in elves:
    if e["total"] > max:
        max = e["total"]
print(max)
