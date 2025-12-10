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


def convert_char(s):
    val = 0 if s == "." else 1
    return val

def identity(s):
    return s

# Lines come in like:
# .......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
#
# The first line is the state.
# Subsequent lines are the map.
# 
# For all lines: convert . to 0
# Convert S and ^ to 1
def parse_data(lines) -> (tuple):
    processed_lines = [list(map(convert_char, l)) for l in lines]
    state = processed_lines[0]
    map_matrix = processed_lines[1:]
    return (state, map_matrix)

def remove_dot_lines(map_matrix):
    zeros = [0 for i in range(len(map_matrix[0]))]
    cleaned_map = [row for row in map_matrix if row != zeros]
    return cleaned_map


# State can only contain 0s and 1s
# but intermediate state can contain 2s like:
# [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
#
# Convert any 2s into flanking 1s, so the above becomes:
# [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
def convert_intermediate_state(s) -> (tuple):
    converted_state = s
    for i in range(len(s)):
        this_val = s[i]
        if this_val == 2:
            # Add the flanking 1s
            if i > 1:
                converted_state[i-1] = 1
            if i+1 < len(s):
                converted_state[i+1] = 1
            # Replace the 2 with a 0
            converted_state[i] = 0
    return converted_state


def test_convert_intermediate_state():
    sta = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
    exp = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    got = convert_intermediate_state(sta)
    assert got == exp

    sta = [0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0]
    exp = [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    got = convert_intermediate_state(sta)
    assert got == exp

    print("test_convert_intermediate_state PASSED")

def solve_problem(in_state, map_matrix) -> int:
    state = in_state
    count = 0
    row_len = len(map_matrix[0])
    zero_row = [0 for i in range(row_len)]
    for i in range(len(map_matrix)):
        map_row = map_matrix[i]
        if map_row == zero_row:
            continue
        intermediate_state = list(map(add, state, map_row))
        count += sum([1 for b in intermediate_state if b == 2])
        state = convert_intermediate_state(intermediate_state)
        print(f"{i=}, {count=}")
        pass

    return count

def solve_problem_part_2(matrix, ranges) -> list:
    pass

class Node:
    def __init__(self, row:int, col:int, l, r):
        self.row = row
        self.col = col
        self.l = l
        self.r = r

    def __repr__(self):
        dots = "  " * self.row
        srow_col = dots + f"({self.row}, {self.col})"

        if self.l:
            l_open = dots + "l:[\n"
            l_clos = dots + "\n  ]"
            sl = l_open + f"{self.l}" + l_clos
        else:
            sl = "l:[]"
        
        if self.r:
            r_open = dots + "r:[\n"
            r_clos = dots + "\n  ]"
            sr = r_open + f"{self.r}" + r_clos
        else:
            sr = "r:[]"
        return "\n".join([srow_col, sl, sr])

    def visualize_dots(self):
        dots = "." * self.col + "^"
        print(dots)
    
    def depth(self):
        if (self.l != None and self.r != None):
            return max(self.l.depth(), self.r.depth())
        elif (self.l != None):
            return self.l.depth()
        elif (self.r != None):
            return self.r.depth()
        else:
            return self.row

def init_tree(matrix):
    # The first row will have the root
    idx = matrix[0].index(1)
    n = Node(0, idx, None, None)
    build_tree(n, matrix)
    print(n)
    return n


def build_tree(n: Node, matrix: list) -> Node:
    child_row = matrix[n.row+1]
    if n.col-1 > 0 and child_row[n.col-1] == 1:
        n.l = Node(n.row+1, n.col-1, None, None)
        if n.row+1 < len(matrix)-1:
            build_tree(n.l, matrix)
    if n.col+1 < len(child_row) and child_row[n.col+1] == 1:
        n.r = Node(n.row+1, n.col+1, None, None)
        if n.row+1 < len(matrix)-1:
            build_tree(n.r, matrix)


def count_depth_first_tree_traverse(matrix) -> int:
    for i in range(len(matrix)):
        one_indexes = [i for i in range(len(matrix)) if matrix[i] == 1]
    return 0


def test_utils():
    test_convert_intermediate_state()



test = True

if test:
    test_utils()

lines = input_data(test, None)

st = datetime.now()

state, map_matrix = parse_data(lines)

cleaned_map_matrix = remove_dot_lines(map_matrix)



root = init_tree(cleaned_map_matrix)

depth = root.depth()

pass
quit()
result = count_depth_first_traverse(cleaned_map_matrix)

result = solve_problem(state, map_matrix)

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
