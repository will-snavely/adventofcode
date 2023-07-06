def split(xs, p):
    if not xs:
        return
    run = []
    for item in xs:
        if p(item):
            yield run
            run = []
        else:
            run.append(item)
    if len(run) > 0 or p(item[-1]):
        yield run

if __name__ == "__main__":
    with open("inputs/day01") as f:
        runs = split(f.readlines(), lambda x: not x.strip())
        sums = [sum(xs) for xs in [[int(x) for x in run] for run in runs]]
        print(max(sums))
        print(sum(sorted(sums)[-3:]))
