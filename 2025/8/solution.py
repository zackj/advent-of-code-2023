from math import sqrt
from datetime import datetime
from util import input_data, read_expected_result, read_expected_result_part_2
from Point import Point, coord_string_to_point

DIST_MAX = 999999999999999999999

def test_utils():
    pass


st = datetime.now()

test = False

if test:
    test_utils()

lines = input_data(test, None)
points = []
for i in range(len(lines)):
    p = coord_string_to_point(lines[i])
    p.id = i
    points.append(p)

num_points = len(points)

print('Calculate distance matrix')
distance_matrix = [[-1 for i in range(num_points)] for j in range(num_points)]

# Use any distance for min_dist to start with
max_dist = DIST_MAX * -1
max_coord = (-1,-1)
min_dist = DIST_MAX
min_coord = (-1, -1)
for i in range(num_points):
    for j in range(num_points):
        if i == j:
            distance_matrix[i][j] = 0
            continue
        p1 = points[i]
        p2 = points[j]
        dist = p1.distance_from_point(p2)
        if dist > max_dist:
            max_dist = dist
            max_coord = (i, j)
        if dist < min_dist:
            min_dist = dist
            min_coord = (i, j)
        distance_matrix[i][j] = dist

print('Done calculating distance matrix')

p1_id = min_coord[0]
p2_id = min_coord[1]
p1 = points[p1_id]
p2 = points[p2_id]
p1.circuit_pts.append(p2)
p2.circuit_pts.append(p1)

iter_limit = 9 if test else 999

for k in range(iter_limit):
    print(f'Calculating pass: {k=}')
    min_dist = DIST_MAX
    min_coord = (-1, -1)
    for i in range(num_points):
        p1 = points[i]
        direct_connections = p1.circuit_pts
        for j in range(num_points):
            if k == 998:
                print(f'998: i, j: {i}, {j}')
            # don't examine yourself.
            if i == j:
                continue
            # don't examine if it's already connected directly
            p2 = points[j]
            if p2 in direct_connections:
                continue

            dist = distance_matrix[i][j]
            if dist < min_dist:
                min_dist = dist
                min_coord = (i, j)
        
    p1_id = min_coord[0]
    p2_id = min_coord[1]
    p1 = points[p1_id]
    p2 = points[p2_id]
    p1.circuit_pts.append(p2)
    p2.circuit_pts.append(p1)

print("finished calculations")
circuits = {}
already_counted_points = set()

for i in range(num_points):
    p = points[i]
    if p in already_counted_points:
        continue
    nodes = p.nodes_in_circuit()
    circuits[i] = nodes
    already_counted_points |= nodes

circuit_counts = sorted([len(circuits[i]) for i in circuits.keys()], reverse=True)

product = 1
for i in range(3):
    product = product * circuit_counts[i]

print(f'{product=}')


et = datetime.now()
td = et-st

if (test):
    expected_result = read_expected_result(None)
    if product != expected_result:
        print(f"PART 1 FAILED. Got '{str(product)}' Expected '{str(expected_result)}'")
        assert False
    else:
        print(f"PART 1 PASSED! Got {str(product)}")

print(f"PART 1 Result: {str(product)}")
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
