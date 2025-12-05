from time import process_time
import pathlib
from datetime import datetime


# Read in the data from a text file and strip out newlines.
def input_data(test_mode: bool, i: int) -> list:
    if test_mode:
        file_name = "test_input" + ("" if i == None else str(i)) + ".txt"
    else:
        file_name = "input" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return lines

def read_expected_result(i: int) -> int:
    file_name = "test_result" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return int(lines[0])

def read_expected_result_part_2(i: int) -> int:
    file_name = "test_result_part2" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return int(lines[0])


def range_stop(r: range):
    return r.stop

# Range values in input can overlap.
# for input:
# 3-5
# 10-14
# 16-20
# 12-18
#
# We need to identify the full ranges:
# 3-5
# 10-20
# 
# 3-5 contains 3, 4, 5 and does not overlap with the others
#
# 10-14 contains 10, 11, 12, 13, 14
# 16-20 contains                         16, 17, 18, 19, 20
# 12-18 contains         12, 13, 14, 15, 16, 17, 18
# So the total range is 10-20 for those three rows.
#
# So compiled ranges are:
# NOTE: ranges are inclusive of final value, hence + 1
# range(3, 5+1)
# range(10, 20+1)
#
# and range values are:
# 3, 4, 5
# 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
def compile_ranges(range_limits):
    ranges = []
    for (a, b) in range_limits:
        start_range_idx = -1
        end_range_idx = -1
        
        # It's possible for an existing range to be entirely
        # contained inside this new limit
        subtended_range_idexes = []

        for i in range(len(ranges)):
            r = ranges[i]
            if a in r:
                # Found a range that includes our start
                assert start_range_idx == -1
                start_range_idx = i
            
            if b in r:
                # Found a range that includes our end
                assert end_range_idx == -1
                end_range_idx = i
            
            if a < r.start and b > r.stop:
                assert start_range_idx == -1 and end_range_idx == -1
                subtended_range_idexes.append(i)
        
        if start_range_idx == -1 and end_range_idx == -1:
            # We need a new range.
            # Ranges need to be inclusive, though, so add 1 to b
            r = range(a,b+1)
            ranges.append(r)

        elif start_range_idx == -1 and end_range_idx != -1:
            # We've found a new lower bound for the end_range
            # Replace end_range with a new one with a lower bound
            end_range = ranges[end_range_idx]
            r = range(a, end_range.stop)
            ranges[end_range_idx] = r

        elif start_range_idx != -1 and end_range_idx == -1:
            # We've found a new upper bound for the start_range
            start_range = ranges[start_range_idx]
            r = range(start_range.start, b+1)
            ranges[start_range_idx] = r

        else:
            # A start_range and an end_range were found.
            # 
            # If those are the same range, do nothing, 
            # since the range at that index contained all the
            # values for the range limits already
            #
            # If they're not the same, combine the ranges.
            if start_range_idx != end_range_idx:
                start_range = ranges[start_range_idx]
                end_range = ranges[end_range_idx]
                r = range(start_range.start, end_range.stop)
                ranges[end_range_idx] = range(0)
                ranges[start_range_idx] = range(0)
                ranges.append(r)
            else:
                #print(f"nothing to do for limits {a} {b}")
                pass

        # Invalidate any subtended ranges
        for i in subtended_range_idexes:
            ranges[i] = range(0)
    
    cleaned_ranges = [r for r in ranges if r != range(0)]

    return sorted(cleaned_ranges, key=range_stop)


def test_compile_ranges():
    # Test where a range is already inside another
    range_limits = [(3, 5), (10, 20), (16, 20),]
    exp = [range(3, 6), range(10,21)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Simple case
    range_limits = [(3, 5)]
    exp = [range(3, 6)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Tests the case where 3 ranges are created, then two are combined
    range_limits = [(3, 5), (10, 14), (16, 20), (12, 18)]
    exp = [range(3, 6), range(10, 21)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Tests the case where a range is replaced by an enclosing one
    range_limits = [(3, 5), (10, 14), (8, 20)]
    exp = [range(3, 6), range(8, 21)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Tests the case where all ranges are replaced
    range_limits = [(3, 5), (10, 14), (8, 20), (1,40)]
    exp = [range(1, 41)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Same test, different order
    range_limits = [(3, 5),  (1, 40), (10, 14), (8, 20)]
    exp = [range(1, 41)]
    got = compile_ranges(range_limits)
    assert got == exp
    
    # Tests the case where a range.start is extended down
    range_limits = [(3, 5), (10, 14), (8, 12)]
    exp = [range(3, 6), range(8,15)]
    got = compile_ranges(range_limits)
    assert got == exp

    # Tests the case where a range.stop is extended up
    range_limits = [(3, 5), (10, 14), (10, 25)]
    exp = [range(3, 6), range(10, 26)]
    got = compile_ranges(range_limits)
    assert got == exp


    print("compile_ranges PASSED")
    


def parse_data(lines) -> tuple:
    # a single empty line separates ranges and ingredients
    sep = lines.index("")
    
    range_limits = [(int(a), int(b)) for (a, b) in [s.split("-") for s in lines[:sep]]]
    fresh_ranges = compile_ranges(range_limits)
    
    ingredients = [int(s) for s in lines[sep+1:]]
    return (fresh_ranges, ingredients)


def count_fresh_ingredients(fresh_ranges) -> int:
    count = sum([len(r) for r in fresh_ranges])
    return count

def count_fresh_ingredients_in_list(fresh_ranges, ingredient_ids) -> int:
    fresh_ingredients = []
    for n in ingredient_ids:
        for r in fresh_ranges:
            if n in r:
                fresh_ingredients.append(n)
                break
    
    return len(fresh_ingredients)

def test_utils():
    test_compile_ranges()



test = False

if test:
    test_utils()

data = input_data(test, None)

st = datetime.now()

fresh_ranges, ingredient_ids = parse_data(data)

result = count_fresh_ingredients_in_list(fresh_ranges, ingredient_ids)

et = datetime.now()
td = et-st

if (test):
    expected_result = read_expected_result(None)
    if result != expected_result:
        print(f"PART 1 FAILED. Got '{str(result)}' Expected '{str(expected_result)}'")
        assert False
    else:
        print(f"PART 1 PASSED! Got {str(result)}")

print(f"PART 1 Result: {str(result)}")
print(f"PART 1 TIME: {td.total_seconds():.7f} seconds")

st = datetime.now()

result_2 = count_fresh_ingredients(fresh_ranges)

et = datetime.now()
td = et-st

if (test):
    expected_result = read_expected_result_part_2(None)
    if result_2 != expected_result:
        print(f"PART 2 FAILED. Got '{str(result_2)}' Expected '{str(expected_result)}'")
        assert False
    else:
        print(f"PART 2 PASSED! Got {str(result_2)}")

print(f"PART 2 Result: {str(result_2)}")
print(f"PART 2 TIME: {td.total_seconds():.7f} seconds")
