#answer = 12560

#filename = 'sample02.txt'
filename = 'input.txt'

x = 1
cycle = 0

total = 0
with open(filename, "r") as f:
    for line in f:
        if line.strip() == "noop":
            cycle += 1
            if cycle in [20, 60, 100, 140, 180, 220]:
                total += cycle * x
                #print(cycle, cycle * x, x)
        else:
            amount = int(line.strip().split()[1])
            for _ in range(2):
                cycle += 1
                if cycle in [20, 60, 100, 140, 180, 220]:
                    total += cycle * x
                    #print(cycle, cycle * x, x)
            x += amount

print(total)
