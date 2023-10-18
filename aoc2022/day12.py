import collections

def part1(grid, start, end):
    queue = collections.deque()
    queue.append((start, 0))
    visited = set()
    adj = [(0,1), (0,-1), (1,0), (-1,0)]

    while queue:
        ((r,c), steps) = queue.popleft()
        if (r,c) in visited:
            continue
        else:
            visited.add((r,c))
        
        if (r,c) == end:
            return steps

        cv = grid[(r,c)]
        for (dr, dc) in adj:
            nr, nc = r + dr, c + dc
            nv = grid[nr, nc]
            if nv > 0 and (nv <= cv or nv == cv + 1): 
                queue.append(((nr,nc), steps + 1))

if __name__ == "__main__":
    with open("aoc2022/inputs/day12") as f:
        lines = [line.strip() for line in f]
        grid = collections.defaultdict(int)
        starts = []
        end = None
        for row in range(0, len(lines)):
            for col in range(0, len(lines[0])):
                c = lines[row][col]
                value = ord(c)
                if c == "S" or c == "a":
                    starts.append(((row,col), c))
                    value = ord("a")
                elif c == "E":
                    end = (row, col)
                    value = ord('z')
                grid[(row, col)] = value 
    
        dists = []
        for (coord, mark) in starts:
            d = part1(grid, coord, end)
            if mark == 'S':
                print("Part 1:", d)
            if d:
                dists.append(d)
        print("Part 2:", min(dists))