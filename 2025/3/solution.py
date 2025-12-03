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

# Convert strings like "12345" to a list
# of integers: [1, 2, 3, 4, 5]
def parse_data(lines) -> list:
    banks = []
    for l in lines:
        characters = list(l)
        banks.append(list([int(s) for s in characters]))
    return banks


# Find the maximum value of in_list and return
# that value and the first index at which it appears
#
# in_list is the list you're seeking through
# abs_max is the maximum value in your range
# so for single digits abs_max is 9.
def max_and_idx(in_list, abs_max) -> tuple:
    idx = 0
    max_value = in_list[idx]
    
    for i in range(1, len(in_list)):
        # 9 is the highest you can get,
        # so if you've found a 9 yer done.
        if max_value == abs_max:
            break
        this_value = in_list[i]
        if this_value > max_value:
            max_value = this_value
            idx = i
    
    return (max_value, idx)

def test_max_and_idx():
    b = [9, 5, 8, 7, 6, 1, 1]
    max_value, max_idx = max_and_idx(b, 9)
    assert max_value == 9
    assert max_idx == 0
    
    b = [4, 8, 5, 8, 7, 6, 1, 1]
    max_value, max_idx = max_and_idx(b, 9)
    assert max_value == 8
    assert max_idx == 1

    b = [4, 5, 7]
    max_value, max_idx = max_and_idx(b, 9)
    assert max_value == 7
    assert max_idx == 2

    print("test_max_and_idx PASSED")




def process_part_1(banks) -> int:
    total = 0
    for b in banks:
        # b is like [9, 5, 8, 7, 6, 1, 1]
        # for that b, we identify 9 as the first digit
        # and 8 as the second digit, for a value of 98.
        # 
        # Seek through b[:-1] for the highest value element.
        # We exclude the last item because we need at least
        # one element after our high_max for the second digit.
        high_max, high_max_idx = max_and_idx(b[:-1], 9)
        low_max, low_max_idx = max_and_idx(b[high_max_idx+1:], 9)

        this_val = high_max * 10 + low_max
        total += this_val
    
    return total


def process_part_2(banks) -> int:
    digit_limit = 12
    total = 0
    for b in banks:
        # b is like  [9, 2, 8, 7, 6, 5, 8]
        # if digit_limit is 4 then we identify: [9, 8, 7, 8]
        # 
        # running_idx = 0
        # Iteration 1: 
        # We need 4 more digits so we ignore the last
        # 3 digits of input to guarantee enough length.
        # examine b[running_idx:-3] = [9, 2, 8, 7]
        # return: max = 9, idx = 0
        # running_idx += (idx + 1) = 1
        #
        # Iteration 2:
        # We need 3 more digits so we ignore the last
        # 2 digits of input to guarantee enough length.
        # examine b[running_idx:-2] = [2, 8, 7, 6]
        # return: max = 8, idx = 1
        # running_idx += (idx + 1) = 3
        #
        # Iteration 3:
        # We need 2 more digits so we ignore the last
        # 1 digits of input to guarantee enough length.
        # examine b[running_idx:-1] = [7, 6, 5]
        # return: max = 7, idx = 0
        # running_idx += (idx + 1) = 4
        #
        # Iteration 4:
        # We need 1 more digits so we ignore the last
        # 0 digits of input to guarantee enough length.
        # examine b[running_idx:] = [6, 5, 8]
        # return: max = 8, idx = 2
        # running_idx += (idx + 1) = 7
        #
        # We identified these maxes: [9, 8, 7, 8]
        # for a total value of 9878

        max_values = []        
        running_idx = 0

        # i is counting up from negative digit_limit.
        # IE: -11, -10, -9... 0
        for i in range(-1*(digit_limit-1), 1):
            if i == 0:
                examine_list = b[running_idx:]
            else:
                examine_list = b[running_idx:i]
            cur_max, cur_max_idx = max_and_idx(examine_list, 9)
            running_idx += (cur_max_idx + 1)
            max_values.append(cur_max)

        this_total = 0
        for i in range(len(max_values)):
            this_digit = max_values[i]
            e = digit_limit-1-i
            this_val = this_digit * 10**e
            this_total += this_val

        total += this_total

    return total
    
    
    



test = False

if test:
    test_max_and_idx()

data = input_data(test, None)

st = process_time()

banks = parse_data(data)

result = process_part_1(banks)

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

result_2 = process_part_2(banks)

et = process_time()
t_part_2 = et-st

if (test):
    expected_result = read_expected_result_part_2(None)
    if result_2 != expected_result:
        print(
            f"PART 2 FAILED. Got '{str(result_2)}' Expected '{str(expected_result)}'")
    else:
        print(f"PART 2 PASSED! Got {str(result_2)}")

print(f"PART 2 Result: {str(result_2)}")
print(f"PART 2 Time: {t_part_2:.2e}")