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


def remove_dot_lines(matrix):
    dots = "." * len(matrix[0])
    cleaned_matrix = [row for row in matrix if row != dots]
    return cleaned_matrix


def test_utils():
    pass


def print_matrix(matrix):
    for row in matrix:
        print(f"row")

# matrix is like:
# '.......^.......'
# '......^.^......'
# '.....^.^.^.....'
def depth_first_count_nodes(r, c, matrix):
    row = matrix[r]
    val = row[c]
    print(f"{r=}, {c=}, {val=}")
    print_matrix(matrix)
    count = 0
    if val == "^":
        count = 1
        # Mark this element as counted by changing
        # it from "^" to "@"
        new_row = row[:c] + "@" + row[c+1:]
        matrix[r] = new_row
        if len(matrix) > r+1 and c-1 >= 0:
            count += depth_first_count_nodes(r+1, c-1, matrix)
        if len(matrix) > r+1 and c+1 < len(row):
            count += depth_first_count_nodes(r+1, c+1, matrix)
    return count


# sol2 is no good. 1202 is too low an answer.

test = False

if test:
    test_utils()

lines = input_data(test, None)

st = datetime.now()

state, map_matrix = parse_data(lines)

print_matrix(map_matrix)
cleaned_matrix = remove_dot_lines(map_matrix)

start_idx = state.index("S")

result = depth_first_count_nodes(0, start_idx, cleaned_matrix)

print("=-=-=-=-=-=")

print_matrix(cleaned_matrix)

print(result)

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
