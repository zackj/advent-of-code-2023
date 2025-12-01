from os import path
from time import process_time
import pathlib
from operator import add, sub




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

def read_expected_result(i: int) -> list:
    file_name = "test_result" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return int(lines[0])


def read_expected_result_part_2(i: int) -> list:
    file_name = "test_result_part2" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return int(lines[0])

def parse_data(data) -> list:
    ops_and_values = []
    for i in range(len(data)):
        s = data[i]
        lr = s[0]
        val = int(s[1:])
        if lr == "R":
            op = add
        else:
            op = sub
        ops_and_values.append((op, val))
        
    return ops_and_values


def process_part_1(ops_and_values):
    count = 0
    cur_value = 50
    for i in range(len(ops_and_values)):
        op = ops_and_values[i][0]
        val = ops_and_values[i][1]
        new_value = op(cur_value, val)
        cur_value = new_value % 100
        if cur_value == 0:
            count += 1
    return count


def process_part_2(ops_and_values):
    count = 0
    cur_value = 50
    for i in range(len(ops_and_values)):
        op = ops_and_values[i][0]
        val = ops_and_values[i][1]

        start_value = cur_value

        # How many times will we sweep through 0
        sweeps_zero_count = val // 100

        # Modulo is commutative, so go ahead and mod the val now
        val_after_sweeping = val % 100

        count += sweeps_zero_count

        new_value = op(cur_value, val_after_sweeping)

        # Check to see if we swept through 0 with this operation
        if start_value != 0 and (new_value < 0 or new_value > 100):
            count += 1

        # Check to see if we landed at 0
        cur_value = new_value % 100

        # Edge Case: we started at 0 and the sweeps landed us at 0 again,
        # meaning the val was a multiple of 100 (val % 100 = 0), then
        # we've already counted this one.
        if (cur_value == 0 and 
            (start_value == 0 and val_after_sweeping == 0) == False):
            count += 1

    return count




test = False

data = input_data(test, None)

st = process_time()

ops_and_values = parse_data(data)

result = process_part_1(ops_and_values)

et = process_time()
t_part_1 = et-st


if (test):
    expected_result = read_expected_result(None)
    if result != expected_result:
        print(f"PART 1 FAILED. Got '{str(result)}' Expected '{str(expected_result)}'")
    else:
        print(f"PART 1 PASSED! Got {str(result)}")

print(f"PART 1 Result: {str(result)}")
print(f"PART 1 Time: {t_part_1:.2e}")

st = process_time()

result_2 = process_part_2(ops_and_values)

et = process_time()
t_part_2 = et-st

if (test):
    expected_result = read_expected_result_part_2(None)
    if result_2 != expected_result:
        print(
            f"PART 2 FAILED. Got '{str(result)}' Expected '{str(expected_result)}'")
    else:
        print(f"PART 2 PASSED! Got {str(result)}")

print(f"PART 2 Result: {str(result_2)}")
print(f"PART 2 Time: {t_part_2:.2e}")







from time import process_time
st = process_time()
# Do the work
et = process_time()
total_time = et-st
print(f"Time: {total_time:.2e}")
