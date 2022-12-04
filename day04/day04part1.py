#answer = 490

#filename = 'sample01.txt'
filename = 'input.txt'

score = 0
with open(filename, "r") as f:
    for line in f:
        [s1,s2] = line.strip().split(',')
        #print(line.strip().split(','))
        #print(s1)
        [s1a, s1b] = map(int, s1.split("-"))
        [s2a, s2b] = map(int, s2.split("-"))
        if s1a<=s2a and s1b>=s2b:
            score += 1
        elif s1a>=s2a and s1b<=s2b:
            score += 1
print(score)

