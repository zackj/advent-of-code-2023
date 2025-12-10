from math import sqrt
from datetime import datetime
import numpy as np
from numpy import unravel_index
from util import input_data, read_expected_result, read_expected_result_part_2

def parse_data(lines):
    point_list = []
    for l in lines:
        x,y = l.split(',')
        point_list.append(int(x))
        point_list.append(int(y))
    
    point_vector = np.array(point_list)
    return point_vector


def swap(x, y):
    return (y, x)

def build_dx_dy_matrix(v):
    num_points = int(len(v)/2) # since each point is two values
    m = np.zeros((num_points-1, len(v)), dtype=int)
    point_idxes = np.array([i for i in range(num_points)])
    for i in range(num_points-1):
        w = np.roll(v, shift=2*(i+1))
        point_idxes = np.roll(point_idxes, shift=1)
        dv = abs(v-w)
        
        # dv is the differential between points x and y
        # but right now the order is confusing.
        # 
        # With test data: 
        # v = [7, 1,   11, 1,   11, 7,    9, 7,   9, 5,   2, 5,   2, 3,   7, 3]
        # w = [7, 3,    7, 1,   11, 1,   11, 7,   9, 7,   9, 5,   2, 5,   2, 3]
        # dv= [0, 2,    4, 0,    0, 6,    2, 0,   0, 2,   7, 0,   0, 2,   5, 0]
        # pt    0-7,    1-0,     2-1,     3-2,    4-3,    5-4,    6-5,    7-6
        # 
        # That last row is telling us what points we divided with the operation
        # so the first point is point 0 minus point 7
        
        for j in range(0, len(v)-1, 2):
            dx = dv[j]
            dy = dv[j+1]
            r = j//2
            c = point_idxes[j//2]
            # we're only populating the upper right side of the matrix, so make
            # sure that row is less than column
            if r > c:
                r, c = swap(r, c)
            #print(f'{r},{c} == {dx}, {dy}')
            m[r][c*2] = dx
            m[r][c*2+1] = dy
    
    # m is a matrix of differentials between points,
    # but right now the order is confusing.
    # For the below, m-n means point m minus point n
    # m[0] = [0-7, 1-0, 2-1, 3-2, 4-3, 5-4, 6-5, 7-6]
    
    return m


def calculate_area_matrix(dxdy):
    area_matrix = np.zeros((len(dxdy)+1, len(dxdy)+1), dtype=int)
    for i in range(len(dxdy)):
        v = dxdy[i][2+(i*2):]
        m = [(v[i]+1)*(v[i+1]+1) for i in range(0, len(v), 2)]
        z = [0 for i in range(i+1)]
        a = np.array(z+m)
        area_matrix[i] = a
        
    return area_matrix



def test_utils():
    x, y = (1, 2)
    x, y = swap(x, y)
    assert (x, y) == (2, 1)
    pass

test = False

if test:
    test_utils()

st = datetime.now()

lines = input_data(test, None)
point_vector = parse_data(lines)

num_points = len(point_vector)/2

# This matrix has all zeros on the diagonal and below
# It represents dx dy for each point pair
# Examples:
#  For points 0 and 7, dx is 0 and dy is 2
#  For points 3 and 5, dx is 7 and dy is 2
#      0   1   2   3   4   5   6   7
# 0 [0 0 4 0 4 6 2 6 2 4 5 4 5 2 0 2]
# 1 [0 0 0 0 0 6 2 6 2 4 9 4 9 2 4 2]
# 2 [0 0 0 0 0 0 2 0 2 2 9 2 9 4 4 4]
# 3 [0 0 0 0 0 0 0 0 0 2 7 2 7 4 2 4]
# 4 [0 0 0 0 0 0 0 0 0 0 7 0 7 2 2 2]
# 5 [0 0 0 0 0 0 0 0 0 0 0 0 0 2 5 2]
# 6 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0]

dxdy_matrix = build_dx_dy_matrix(point_vector)

area_matrix = calculate_area_matrix(dxdy_matrix)

maxindex = area_matrix.argmax()

coord = unravel_index(area_matrix.argmax(), area_matrix.shape)

max_area = area_matrix[coord]

result = int(max_area)

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
