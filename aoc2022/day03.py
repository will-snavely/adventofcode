import functools

def priority(ch):
    if 'a' <= ch <= 'z':
        return ord(ch) - ord('a') + 1
    else:
        return ord(ch) - ord('A') + 27

if __name__ == "__main__":
    with open("inputs/day03") as f:
        lines = [x.strip() for x in f.readlines()]
        prisum = 0
        for line in lines:
            mid = len(line) // 2
            r1 = line[:mid]
            r2 = line[mid:]
            isect = list(set(r1).intersection(set(r2)))
            prisum += priority(isect[0])
        print(prisum)

        idx = 0
        prisum = 0
        sacks = [set(x) for x in lines]
        while idx + 3 <= len(sacks):
            isect = list(functools.reduce(lambda x,y: x.intersection(y), sacks[idx:idx+3]))
            prisum += priority(isect[0])
            idx += 3
        print(prisum)
