#answer = 5340

#filename = 'sample01.txt'
filename = 'input.txt'

total = 0
def parse(s: str):
    #s = s.strip()[1:-1]
    list = []
    currentstack = [list]
    while len(s) > 0:
        if s[0] == ",":
            s = s[1:]
        if s[0].isdigit():
            num = ""
            while s[0].isdigit():
                num += s[0]
                s = s[1:]
            currentstack[-1].append(int(num))
        elif s[0] == "[":
            newlist = []
            currentstack[-1].append(newlist)
            currentstack.append(newlist)
            s = s[1:]
        elif s[0] == "]":
            currentstack.pop()
            s = s[1:]
        else:
            print("Unknown string", s, list, currentstack)
    return list[0]

#print(parse("[1,[2,[3,[4,[5,6,7]]]],8,9]"))
data = []
with open(filename, "r") as f:
    first = f.readline()
    second = f.readline()
    f.readline()
    index = 1
    while first:
        first = parse(first.strip())
        second = parse(second.strip())
        #print(first, second)

        done = False
        rightorder = False
        fcurrentstack = [first]
        scurrentstack = [second]
        while not done:
            #print("Comparing", fcurrentstack[-1], scurrentstack[-1], sep=" *** ")
            if len(fcurrentstack[-1]) == 0 and len(scurrentstack[-1]) == 0:
                fcurrentstack.pop()
                scurrentstack.pop()
            elif len(fcurrentstack[-1]) == 0 and len(scurrentstack[-1]) > 0:
                done = True
                rightorder = True
            elif len(fcurrentstack[-1]) > 0 and len(scurrentstack[-1]) == 0:
                done = True
                rightorder = False
                #print("Too long")
                #print(fcurrentstack[-1])
                #print(scurrentstack[-1])
            elif isinstance(fcurrentstack[-1][0], int) and isinstance(scurrentstack[-1][0], int):
                if fcurrentstack[-1][0] < scurrentstack[-1][0]:
                    done = True
                    rightorder = True
                elif fcurrentstack[-1][0] > scurrentstack[-1][0]:
                    done = True
                    rightorder = False
                    #print(fcurrentstack)
                    #print(scurrentstack)
                else:
                    fcurrentstack[-1].pop(0)
                    scurrentstack[-1].pop(0)
            elif isinstance(fcurrentstack[-1][0], int):
                fcurrentstack[-1][0] = [fcurrentstack[-1][0]]
            elif isinstance(scurrentstack[-1][0], int):
                scurrentstack[-1][0] = [scurrentstack[-1][0]]
            else: # both lists
                fcurrentstack.append(fcurrentstack[-1].pop(0))
                scurrentstack.append(scurrentstack[-1].pop(0))

        print(rightorder)
        if(rightorder):
            total += index
        index += 1
        first = f.readline()
        second = f.readline()
        f.readline()
        #print()
print(total)
    
