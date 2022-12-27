#answer = 2=20---01==222=0=0-2

from functools import reduce


filename = 'sample01.txt'
filename = 'input.txt'


def s2d(s:str) -> int:
    if s == "2" or s == "1" or s == "0":
        return int(s)
    elif s == "-":
        return -1
    elif s == "=":
        return -2
    else:
        assert False, s

def d2s(d:int) -> str:
    assert -2 <= d <= 2
    if d>=0: return str(d)
    if d == -1: return "-"
    if d == -2: return "="
        
def snafu_to_dec(snafu: str) -> int:
    result = 0
    place = 1
    for c in snafu[::-1]:
        result += s2d(c) * place
        place *= 5
    return result
    

def dec_to_snafu(dec: int) -> str:
    absval = abs(dec)
    strval = ""
    values = []
    while absval > 0:
        r = absval%5
        if r>2: r-=5
        values.append(r)
        absval -= r
        absval //= 5

    print("absval=",absval,". values=",values)
       
    for v in values:
        strval = d2s(v) + strval
    return strval


total = 0
with open(filename, "r") as f:
    for line in f:
        total += snafu_to_dec(line.strip())
print(total)
print(dec_to_snafu(total))



