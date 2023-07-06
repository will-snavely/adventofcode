if __name__ == "__main__":
    r = 1
    p = 2
    s = 3
    w = 6
    d = 3
    l = 0

    scoring = {
            r: {r: d, p: l, s: w},
            p: {r: w, p: d, s: l},
            s: {r: l, p: w, s: d}
            }

    with open("inputs/day02") as f:
        lines = f.readlines()
        part1_map = { "A": r, "B": p, "C": s, "X": r, "Y": p, "Z": s } 
        score1 = 0
        for line in lines:
            moves = line.strip().split()
            opp = part1_map[moves[0]]
            me = part1_map[moves[1]]
            score1 += scoring[me][opp] + me
        print(score1)

        part2_scoring = {
                "A": { "X": s + l, "Y": r + d, "Z": p + w },
                "B": { "X": r + l, "Y": p + d, "Z": s + w },
                "C": { "X": p + l, "Y": s + d, "Z": r + w }
                }

        score2 = 0
        for line in lines:
            moves = line.strip().split()
            opp = moves[0]
            me = moves[1]
            score2 += part2_scoring[opp][me]
        print(score2)

