from time import process_time
import pathlib

# Read in the data from a text file and strip out newlines.
def input_data(test_mode: bool, i: int) -> list:
    if test_mode:
        file_name = "test_input" + ("" if i == None else str(i)) + ".txt"
    else:
        file_name = "input" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines

def read_expected_result(i: int) -> int:
    file_name = "test_result" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return int(lines[0])


def read_expected_result_part_2(i: int) -> int:
    file_name = "test_result_part2" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return int(lines[0])

# convert a 2d array like the following
#
#   ..@@.@@@@.
#   @@@.@.@.@@
#   @@@@@.@.@@
#
# Into a 1d array: ..@@.@@@@.@@@.@.@.@@@@@@@.@.@@
#
# Caller is responsible for sending well-formed input
#
# return (num_rows, num_cols, unwrapped) where
# num_rows is the number of rows
# num_cols is the number of columns
# unwrapped is the 2d array converted to 1d
def unwrap_array(a) -> tuple:
    num_rows = len(a)
    num_cols = len(a[0]) if (num_rows > 0) else 0
    unwrapped = []
    for aRow in a:
        unwrapped.extend(list(aRow))
    return (num_rows, num_cols, unwrapped)

def test_unwrap_array():
    test_data = []
    num_rows, num_cols, unwrapped = unwrap_array(test_data)
    assert num_rows == 0
    assert num_cols == 0
    assert unwrapped == test_data

    test_data = [[1]]
    num_rows, num_cols, unwrapped = unwrap_array(test_data)
    assert num_rows == 1
    assert num_cols == 1
    assert unwrapped == [1]

    test_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 1, 2]]
    num_rows, num_cols, unwrapped = unwrap_array(test_data)
    assert num_rows == 4
    assert num_cols == 3
    assert unwrapped == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

    print("test_unwrap_array PASSED")


def parse_data(lines) -> tuple:
    return unwrap_array(lines)

# Given an (row,col) coordinate for a 2d array
# return an integer index of the element in the
# unwrapped 1d array.
# 
# A 2d input array like this:
#
#   abcd
#   efgh
#   ijkl
#
# Is represented unwrapped as:
#   abcdefghijkl
# 
# (0,0) -> 0
# (0,1) -> 1
# (0,2) -> 2
# (0,3) -> 3
# (1,0) -> 4
# (1,1) -> 5


def point_to_unwrapped_idx(row, col, num_cols) -> int:
    idx = num_cols*row + col
    return idx

# Take an index for the unwrapped 1d array
# and convert it into the equivalent point
# in the 2d array
def unwrapped_idx_to_point(idx, num_rows, num_cols) -> tuple:
    row = idx // num_cols
    col = idx - (row * num_cols)
    return (row, col)


def test_point_to_unwrapped_idx():
    a = [["a", "b", "c", "d"],
         ["e", "f", "g", "h"],
         ["i", "j", "k", "l"]]
    num_rows, num_cols, unwrapped = unwrap_array(a)

    for row in range(num_rows):
        for col in range(num_cols):
            idx = point_to_unwrapped_idx(row, col, num_cols)
            u_val = unwrapped[idx]
            a_val = a[row][col]
            assert u_val == a_val


def test_unwrapped_idx_to_point():
    a = [["a", "b", "c", "d"],
         ["e", "f", "g", "h"],
         ["i", "j", "k", "l"]]
    num_rows, num_cols, unwrapped = unwrap_array(a)

    for i in range(len(unwrapped)):
        row, col = unwrapped_idx_to_point(i, num_rows, num_cols)
        u_val = unwrapped[i]
        a_val = a[row][col]
        assert u_val == a_val

    print("test_unwrapped_idx_to_point PASSED")




# A 2d input array like this:
#
#   abcdefghij
#   klmnopqrst
#   uvwxyz1234
#   567890ABCD
#
# Is represented unwrapped as:
#   abcdefghijklmnopqrstuvwxyz1234567890ABCD
#
# A neighborhod of size n means all the 
# cells within n count of the input
# in the original 2d array. 
# 
# That neighborhood can have a variable number of elements
# depending on where the source cell is.
# 
# For neighborhood size 1, this is all the adjacent cells,
# in which case the num_neighbors can be 3, 5, or 8 elements.
#
# CASE 1: x,y = (0,0) is the top corner of the 2d array
# NUM_NEIGHBORS: 4
# NEIGHBORHOOD: [(0,0), (0,1), (1,0), (1,1)]
# 
# CASE 2: x,y = (0,1) is the second element of the top row
# NUM_NEIGHBORS: 6
# NEIGHBORHOOD: [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
#
# CASE 3: x,y = (1,3) is the fourth element of the second row
# NUM_NEIGHBORS: 9
# NEIGHBORHOOD: [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,2), (2,3), (2,4)]
def neighborhood_points(in_row, in_col, num_rows, num_cols, size) -> list:
    start_row = 0 if in_row-size < 0 else in_row-size
    end_row = num_rows if in_row+size > num_rows else in_row+size
    start_col = 0 if in_col-size < 0 else in_col-size
    end_col = num_cols if in_col+size > num_cols else in_col+size
    
    neighbors = []
    for row in range(start_row, min(num_rows, end_row+1)):
        for col in range(start_col, min(num_cols, end_col+1)):
            neighbors.append((row, col))
    return neighbors


def test_neighborhood_points():
    a = [[0,   1,  2,  3,  4,  5],
         [6,   7,  8,  9, 10, 11],
         [12, 13, 14, 15, 16, 17],
         [18, 19, 20, 21, 22, 23],
         [24, 25, 26, 27, 28, 29],
         [30, 31, 32, 33, 34, 35]]
    num_rows, num_cols, unwrapped = unwrap_array(a)
    
    size = 1
    row = 0
    col = 0
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 0), (0, 1),
                 (1, 0), (1, 1)]

    row = 0
    col = 1
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2)]

    row = 1
    col = 3
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 2), (0, 3), (0, 4),
                 (1, 2), (1, 3), (1, 4),
                 (2, 2), (2, 3), (2, 4)]

    row = 5
    col = 5
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(4, 4), (4, 5),
                 (5, 4), (5, 5)]

    # Test for Size 2
    size = 2
    row = 0
    col = 0
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2),
                 (2, 0), (2, 1), (2, 2)]

    row = 0
    col = 1
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 0), (0, 1), (0, 2), (0, 3),
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3)]

    row = 1
    col = 3
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                 (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]
    
    row = 3
    col = 3
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                 (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                 (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
                 (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]

    row = 5
    col = 5
    n = neighborhood_points(row, col, num_rows, num_cols, size)
    assert n == [(3, 3), (3, 4), (3, 5),
                 (4, 3), (4, 4), (4, 5),
                 (5, 3), (5, 4), (5, 5)]
    
    print("test_neighborhood_points PASSED")


def neighborhood_indexes(in_idx, num_rows, num_cols, size) -> list:
    row, col = unwrapped_idx_to_point(in_idx, num_rows, num_cols)
    nhood_points = neighborhood_points(row, col, num_rows, num_cols, size)
    indexes = [point_to_unwrapped_idx(row, col, num_cols) for (row,col) in nhood_points]
    return indexes

def test_neighborhood_indexes():
    a = [[0,   1,  2,  3,  4,  5],
         [6,   7,  8,  9, 10, 11],
         [12, 13, 14, 15, 16, 17],
         [18, 19, 20, 21, 22, 23],
         [24, 25, 26, 27, 28, 29],
         [30, 31, 32, 33, 34, 35]]
    num_rows, num_cols, unwrapped = unwrap_array(a)

    idx = 1
    nhood_indexes = neighborhood_indexes(idx, num_rows, num_cols, 1)
    assert nhood_indexes == [0, 1, 2, 6, 7, 8]

    size = 1
    idx = 1
    nhood_indexes = neighborhood_indexes(idx, num_rows, num_cols, size)
    assert nhood_indexes == [0, 1, 2, 6, 7, 8]

    size = 2
    idx = 20
    nhood_indexes = neighborhood_indexes(idx, num_rows, num_cols, size)
    assert nhood_indexes == [6,  7,  8,  9, 10,
                             12, 13, 14, 15, 16,
                             18, 19, 20, 21, 22,
                             24, 25, 26, 27, 28,
                             30, 31, 32, 33, 34]

    print("test_neighborhood_indexes PASSED")


# An index is accessible if its neighborhood contains
# less than 4 @s
def get_accessible_indexes(num_rows, num_cols, unwrapped) -> list:
    accessible_indexes = [] 
    for i in range(len(unwrapped)):
        # Don't check the dots, only the @s
        if unwrapped[i] != "@":
            continue

        nhood_indexes = neighborhood_indexes(i, num_rows, num_cols, 1)

        # nhood_indexes includes this index,m so remove it.
        nhood_indexes.remove(i)

        nhood_values = [unwrapped[j] for j in nhood_indexes]
        num_ats = sum(s == "@" for s in nhood_values)
        if num_ats < 4:
            accessible_indexes.append(i)

    return accessible_indexes


def process_part_1(num_rows, num_cols, unwrapped) -> list:
    accessible_indexes = get_accessible_indexes(num_rows, num_cols, unwrapped)
    return accessible_indexes


def process_part_2(accessible_indexes, num_rows, num_cols, unwrapped) -> int:
    count_removed = 0
    while len(accessible_indexes) > 0:
        # Remove any @s that are accessible by replacing them with .
        for i in accessible_indexes:
            unwrapped[i] = "."
        count_removed += len(accessible_indexes)
        accessible_indexes = get_accessible_indexes(num_rows, num_cols, unwrapped)
    
    return count_removed



test = False

if test:
    test_unwrap_array()
    test_point_to_unwrapped_idx()
    test_unwrapped_idx_to_point()
    test_neighborhood_points()
    test_neighborhood_indexes()

data = input_data(test, None)

st = process_time()

num_rows, num_cols, unwrapped = parse_data(data)

accessible_indexes = process_part_1(num_rows, num_cols, unwrapped)

result = len(accessible_indexes)

et = process_time()
t_part_1 = et-st

if (test):
    expected_result = read_expected_result(None)
    if result != expected_result:
        print(f"PART 1 FAILED. Got '{str(result)}' Expected '{str(expected_result)}'")
        assert False
    else:
        print(f"PART 1 PASSED! Got {str(result)}")

print(f"PART 1 Result: {str(result)}")
print(f"PART 1 TIME: {t_part_1:.4} seconds")

st = process_time()

result_2 = process_part_2(accessible_indexes, num_rows, num_cols, unwrapped)

et = process_time()
t_part_2 = et-st

if (test):
    expected_result = read_expected_result_part_2(None)
    if result_2 != expected_result:
        print(f"PART 2 FAILED. Got '{str(result_2)}' Expected '{str(expected_result)}'")
        assert False
    else:
        print(f"PART 2 PASSED! Got {str(result_2)}")

print(f"PART 2 Result: {str(result_2)}")
print(f"PART 2 TIME: {t_part_2:.4} seconds")
