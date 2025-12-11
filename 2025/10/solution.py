from math import sqrt
from datetime import datetime
import numpy as np
import itertools as it
from util import input_data, read_expected_result, read_expected_result_part_2


def dot_pound_to_bin(s):
    if s == '.':
        return 0
    elif s == '#':
        return 1
    else:
        assert False


def bin_to_dot_pound(i):
    if i == 0:
        return '.'
    elif i == 1:
        return '#'
    else:
        assert False

class BinaryVector:
    def __init__(self, len, indexes, is_indicator=False):
        self.v = np.zeros(len, dtype=int)
        self.indexes = indexes
        self.is_indicator = is_indicator
        for i in indexes:
            self.v[i] = 1
    
    def __repr__(self):
        s = ''.join([str(i) for i in list(self.v)])
        s += ' ' + str(self.indexes)
        if self.is_indicator:
            s += ' ' + self.dot_pound_str()
        return s
    
    def dot_pound_str(self):
        s = ''.join(list(map(bin_to_dot_pound, list(self.v))))
        return s





def parse_data(lines):
    # line is like:
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    details = []
    for l in lines:
        i_start = l.index('[')
        i_stop = l.index(']')
        ind_part = l[i_start+1:i_stop]
        ind_length = len(ind_part)

        indicator_indexes = [i for i in range(len(ind_part)) if ind_part[i] == '#']
        
        indicator = BinaryVector(ind_length, indicator_indexes, True)
        # print(f'{indicator=}')

        j_start = l.index('{')
        j_part = l[j_start+1:-1]
        joltage = [int(s) for s in j_part.split(',')]
        # print(f'{joltage=}')

        button_part = l[i_stop+2:j_start-1]
        button_strings = [s.strip().strip('(').strip(')') for s in button_part.split(' ')]
        buttons = []
        for b in button_strings:
            indexes = [int(s) for s in b.split(',')]
            button = BinaryVector(ind_length, indexes)
            # print(f'{button=}')
            buttons.append(button)
        
        details.append((indicator, buttons, joltage))

    return details

def get_least_moves(indicator, buttons):
    i = 1
    while True:
        for t in it.combinations([b.v for b in buttons], i):
            x = np.add.reduce(t) % 2
            if (x == indicator.v).all():
                # print(f'Winning combo for {i=}: {t}')
                return i
        i += 1
        if i % 10000 == 0:
            print(f'iteration {i}')

def test_utils():
    pass

test = False

if test:
    test_utils()

st = datetime.now()

lines = input_data(test, None)
details = parse_data(lines)

move_counts = []
for i in range(len(details)):
    d = details[i]
    indicator = d[0]
    buttons = d[1]
    joltage = d[2]
    num_moves = get_least_moves(indicator, buttons)
    move_counts.append(num_moves)

result = sum(move_counts)

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
