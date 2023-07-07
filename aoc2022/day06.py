import collections

def find_marker(s, size):
    count = collections.defaultdict(int)
    for idx in range(size-1):
        count[s[idx]] += 1
    for idx in range(size-1, len(s)):
        count[s[idx]] += 1
        if all(count[k] in [0,1] for k in count):
            return idx+1
        else:
            count[s[idx-size+1]] -= 1
    return -1

if __name__ == "__main__":
    with open("inputs/day06") as f:
        lines = [x.strip() for x in f.readlines()]
        for line in lines:
            print(find_marker(line, 4))
            print(find_marker(line, 14))
