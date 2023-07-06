from pyparsing import (
    Word, Suppress, Group, tokenMap, nums
)

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        

    def size(self):
        return max(0, self.end - self.start + 1)
       

Integer = Word(nums).setParseAction(tokenMap(int))
RangeTok = (Integer + Suppress("-") + Integer).setParseAction(lambda x: Range(x[0], x[1]))
Ranges = RangeTok + Suppress(",") + RangeTok

def overlap(r1,r2):
    left = max([r1.start, r2.start])
    right = min([r1.end, r2.end]) 
    return Range(left, right)

if __name__ == "__main__":
    with open("inputs/day04") as f:
        lines = [x.strip() for x in f.readlines()]
        count_part1 = 0
        count_part2 = 0
        for line in lines:
            ranges = Ranges.parseString(line)
            olap = overlap(ranges[0], ranges[1])
            if olap.size() > 0:
                count_part2 += 1
                if olap.size()== ranges[0].size() or olap.size() == ranges[1].size():
                    count_part1 += 1
        print(count_part1)
        print(count_part2)
