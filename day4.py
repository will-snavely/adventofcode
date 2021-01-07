import re


def validate_required_fields(passport: dict):
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    diff = required_fields.difference(passport.keys())
    return len(diff) == 0


def validate_part2(passport: dict):
    return validate_required_fields(passport) \
           and validate_byr(passport.get("byr")) \
           and validate_iyr(passport.get("iyr")) \
           and validate_eyr(passport.get("eyr")) \
           and validate_hgt(passport.get("hgt")) \
           and validate_hcl(passport.get("hcl")) \
           and validate_ecl(passport.get("ecl")) \
           and validate_pid(passport.get("pid"))


def validate_byr(byr_raw):
    try:
        byr = int(byr_raw)
        return 1920 <= byr <= 2020
    except:
        return False


def validate_iyr(iyr_raw):
    try:
        iyr = int(iyr_raw)
        return 2010 <= iyr <= 2020
    except:
        return False


def validate_eyr(eyr_raw):
    try:
        eyr = int(eyr_raw)
        return 2020 <= eyr <= 2030
    except:
        return False


def validate_hgt(hgt_raw):
    match = re.match("^(\d+)(cm|in)$", hgt_raw)
    if match:
        height = int(match.group(1))
        unit = match.group(2)
        if unit == "cm":
            return 150 <= height <= 193
        elif unit == "in":
            return 59 <= height <= 76
    return False


def validate_hcl(hcl_raw):
    match = re.match("^#([0-9a-f]){6}$", hcl_raw)
    return match is not None


def validate_ecl(ecl_raw):
    return ecl_raw in \
           {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def validate_pid(pid_raw):
    match = re.match("^[0-9]{9}$", pid_raw)
    return match is not None


def parse_passports(path):
    with open(path) as f:
        cur_passport = {}
        for line in f:
            stripped = line.strip()
            if stripped:
                fields = [item.split(":") for item in stripped.split()]
                for field in fields:
                    cur_passport[field[0]] = field[1]
            else:
                yield cur_passport
                cur_passport = {}


if __name__ == "__main__":
    passports = list(parse_passports("inputs/day4"))
    part1_results = [p for p in passports if validate_required_fields(p)]
    part2_results = [p for p in passports if validate_part2(p)]
    print(len(part1_results))
    print(len(part2_results))
    print(validate_pid("002d45678"))
