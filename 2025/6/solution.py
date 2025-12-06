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


def get_problem_ranges(lines) -> tuple:
    matrix = [list(s) for s in lines]
    row_len = len(matrix[0])
    row_cnt = len(matrix)
    space_row = list(" " * row_cnt)
    div_indexes = [i for i in range(row_len) if [row[i] for row in matrix] == space_row]

    start = 0
    ranges = []
    for i in range(len(div_indexes)):
        stop = div_indexes[i]
        ranges.append(range(start, stop))
        start = stop
    
    # Add the final range
    ranges.append(range(start,row_len))

    return (ranges, matrix)

def product(values):
    p = 1
    for n in values:
        p = p*n
    return p



# Lines come in like:
# "123 328  51 64 "
# " 45 64  387 23 "
# "  6 98  215 314"
# "*   +   *   +  "
#
# Use the calculated ranges to extract each column
# and convert the values to ints
def solve_problems(lines, ranges) -> list:
    operators = lines[-1]
    results = []
    for i in range(len(ranges)):
        r = ranges[i]
        start = r.start
        stop = r.stop
        op = operators[start:stop].strip(" ")
        values = [int(row[start:stop].strip(" ")) for row in lines[:-1]]
        if op == "*":
            results.append(product(values))
        else:
            results.append(sum(values))
    return results
        

def rotate_matrix(matrix):
    rotated = []
    num_cols = len(matrix[0])
    for i in range(num_cols):
        rotated.append([row[i] for row in matrix])
    return rotated

def test_rotate_matrix():
    test = [['1', '2', '3'],
            [' ', '4', '5'],
            [' ', ' ', '6'],
            ['*', ' ', ' ']]
    rotated = rotate_matrix(test)
    exp =  [['1', ' ', ' ', '*'],
            ['2', '4', ' ', ' '],
            ['3', '5', '6', ' ']]
    assert rotated == exp

def value_from_row(row) -> int:
    value = int("".join([s for s in row if s != " "]))
    return value

def test_value_from_row():
    rows = [['1', ' ', ' '], 
            ['2', '4', ' '], 
            ['3', '5', '6']]
    exp = [1, 24, 356]
    for i in range(len(rows)):
        r = rows[i]
        e = exp[i]
        v = value_from_row(r)
        assert v == e

# The same input lines are now in a matrix shaped like this:
# ['1', '2', '3', ' ', '3', '2', '8', ' ', ' ', '5', '1', ' ', '6', '4', ' ']
# [' ', '4', '5', ' ', '6', '4', ' ', ' ', '3', '8', '7', ' ', '2', '3', ' ']
# [' ', ' ', '6', ' ', '9', '8', ' ', ' ', '2', '1', '5', ' ', '3', '1', '4']
# ['*', ' ', ' ', ' ', '+', ' ', ' ', ' ', '*', ' ', ' ', ' ', '+', ' ', ' ']
def solve_problem_part_2(matrix, ranges) -> list:
    results = []
    
    digit_cnt_limit = len(matrix)-1
    operators = matrix[-1]

    for i in range(len(ranges)):
        r = ranges[i]
        start = r.start + (1 if i > 0 else 0)
        stop = r.stop
        sub_matrix = [row[start:stop] for row in matrix]
        # sub_matrix is like this:
        # ['1', '2', '3']
        # [' ', '4', '5']
        # [' ', ' ', '6']
        # ['*', ' ', ' ']
        op = sub_matrix[-1][0]
        
        value_matrix = rotate_matrix(sub_matrix[:-1])
        values = [value_from_row(row) for row in value_matrix]
        
        if op == "*":
            results.append(product(values))
        else:
            results.append(sum(values))
    return results


def test_utils():
    test_rotate_matrix()
    test_value_from_row()



test = False

if test:
    test_utils()

lines = input_data(test, None)

st = datetime.now()

ranges, matrix = get_problem_ranges(lines)

problem_solutions = solve_problems(lines, ranges)

result = sum(problem_solutions)

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
