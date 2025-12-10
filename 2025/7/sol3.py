import pathlib
from datetime import datetime
from operator import add

# Read in the data from a text file and strip out newlines.
def input_data(test_mode: bool, i: int) -> list:
    if test_mode:
        file_name = "test_input" + ("" if i == None else str(i)) + ".txt"
    else:
        file_name = "input" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    input_lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return input_lines

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


# Lines come in like:
# .......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
#
# The first line is the state.
# Subsequent lines are the map.
def parse_data(lines) -> (tuple):
    state = lines[0]
    map_matrix = lines[1:]
    return (state, map_matrix)



def test_utils():
    pass


def print_matrix(matrix):
    for row in matrix:
        print(row)


def replace_char_at_index(s: str, c: str, i: int):
    s = s[:i] + c + s[i+1:]
    return s


# Produce a new row by splitting or perpetuating tachyons
# RULE 1:
#   .......|.......
# + .......^.......
# = ......|.|......
#
# RULE 2:
#   .......|.......
# + ...............
# = .......|.......
#
# Return the new row and the number of splits encountered
def split_tachyons(s1, s2) -> tuple:
    split_count = 0
    r = '.' * len(s1)
    for i in range(len(s1)):
        if s1[i] != '|':
            continue  # This isn't a tachyon
        if s2[i] == '^':
            split_count += 1
            if (i-1 >= 0):
                r = replace_char_at_index(r, '|', i-1)
            if (i+1 < len(r)):
                r = replace_char_at_index(r, '|', i+1)
        elif s2[i] == '.':
            r = replace_char_at_index(r, '|', i)
    return (r, split_count)


def process_matrix(matrix):
    split_count = 0

    for i in range(1, len(matrix), 2):
        # i is indexed to the rows with ^ characters
        this_row = matrix[i]
        last_row = matrix[i-1]  # There is always a prior row
        next_row, new_splits = split_tachyons(last_row, this_row)
        matrix[i+1] = next_row
        split_count += new_splits

        print_matrix(matrix)

    return split_count

test = False

if test:
    test_utils()

lines = input_data(test, None)

st = datetime.now()

state, matrix = parse_data(lines)

print_matrix(matrix)

start_idx = state.index("S")

matrix[0] = replace_char_at_index(matrix[0], '|', start_idx)

split_count = process_matrix(matrix)

print("=-=-=-=-=-=-=-=")

print_matrix(matrix)

print(f"{split_count=}")
result = split_count

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
quit()
st = datetime.now()

problem_solutions = solve_problem_part_2(matrix, ranges)
result_2 = sum(problem_solutions)

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
