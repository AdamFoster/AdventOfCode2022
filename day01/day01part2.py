#answer = 207576

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


elves.sort(key=lambda e: e["total"], reverse=True)

print(elves[0]["total"]+elves[1]["total"]+elves[2]["total"])


