from time import process_time
import pathlib

# Read in the data from a text file and strip out newlines.
def input_data(test_mode: bool, i: int) -> str:
    if test_mode:
        file_name = "test_input" + ("" if i == None else str(i)) + ".txt"
    else:
        file_name = "input" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines[0]

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

def parse_data(in_string) -> list:
    ranges = [ tuple(int(i) for i in s.split("-")) for s in in_string.split(",") ]
    return ranges


# Count the digits in n
# Cases:
# n = 191, return 3
# n = 1000, return 4
# n = 194875, return 6
def number_of_digits(n) -> int:
    e = 1
    while (n % (10**e) != n):
        e += 1
    return e


# We are seeking numbers whose format is a sequence of digits repeated twice.
# Examples are:
# 11
# 22
# 123123
# 95849584
#
# If a number's digit length is odd, it is not a match. IE:
# 249 has three digits, so it cannot possibly be a sequence of digits repeated twice.
# 
# Some ranges can be completely ignored because they never have an even number of digits.
# 0, 1, 2... 8, 9               IGNORE, 1 digit
# 10, 11... 98, 99              CONSIDER, 2 digits
# 100, 101... 998, 999          IGNORE, 3 digits
# 1000, 1001… 9998, 9999        CONSIDER, 4 digits
# 10000, 10001… 99998, 99999    IGNORE, 5 digits
# 100000, 100001… 999999        CONSIDER, 6 digits
# 1000000… 9999999              IGNORE, 7 digits
# 10000000… 99999999            CONSIDER, 8 digits


# Inspect each range, finding sub-ranges that should be considered.
# These sub-ranges are Pythonic, meaning range(a,b) will be 
# every integer from a to b-1.
# 
# CASES:
#   1. Range spans multiple segments with even numbers of digits
#   INPUT: 555, 1000006 then return these ranges:
#   RETURN: [(1000, 10000), (100000, 1000000)]
#   
#   2. Range spans no segments with even numbers of digits
#   INPUT: 123, 555
#   RETURN: []
#   
#   3. Range spans one segment with even number of digits
#   INPUT: 123, 5918
#   RETURN: [(1000, 5919)]
def considerable_ranges(in_range) -> list:
    (n, stop) = in_range
    # n is the current number we're examining
    
    # storage for all the sub ranges we'll be inspecting
    ranges = []

    while (n < stop):
        # count the digits of n
        e = number_of_digits(n)

        # If n has an even number of digits, we're cool
        # otherwise, skip everything from n to the next
        # number with an even number of digits
        if e % 2 != 0:
            n = 10**e
            e += 1

        assert e % 2 == 0

        # If n > stop then we're done.
        # IE: range is 123-555
        # n starts at 123, which has 3 digits so e = 3
        # but since e is odd, we set n = 10**e = 10**3 = 1000
        # but 1000 > 555, so we don't need to inspect this range
        # at all
        if n > stop:
            continue

        # Determine where to stop.
        # IE: range is 123, 100005
        # n starts at 123, which has 3 digits so e = 3
        # but since e is odd, we set n = 10**e = 10**3 = 1000
        # But n < 100005, so we need to inspect all the values from 1000 to 100005
        # but that's actually only the ranges:
        # 1000 - 10000
        # 100000 - 100005
        # but, 10000 to 10005 all have odd number of digits
        # so we don't need to inspect those at all.
        # In this example,
        # stop_e = 6
        stop_e = number_of_digits(stop)

        while (e <= stop_e):
            # set the range
            if e == stop_e:
                ranges.append((n, stop+1))
            else:
                ranges.append((n, min(stop, 10**e)))
            
            e += 1
            n = 10**e
            e += 1
            
    return ranges


def gather_all_considerable_ranges(ranges) -> list:
    consider_ranges = []
    for r in ranges:
        consider_ranges.extend(considerable_ranges(r))
    return consider_ranges


def process_part_1(ranges):
    considerable_ranges = gather_all_considerable_ranges(ranges)
    bad_numbers = []
    for (start, stop) in considerable_ranges:
        # Get the number of digits.
        e = int(number_of_digits(start)/2)
        for i in range(start, stop):
            second_half = i % 10**e
            first_half = (i-second_half) // 10**e
            if first_half == second_half:
                bad_numbers.append(i)
                #print(f"bad number: {i}")
    
    return sum(bad_numbers)

def factorize(n):
    factors = []
    for i in range(1, n+1):
        if n / i % 1 == 0:
            factors.append((i, n // i))
            
    
    return factors

def test_factorize():
    test = [11, 24, 16, 101, 99]
    exp = [[(1, 11), (11, 1)],
           [(1, 24), (2, 12), (3, 8), (4, 6), (6, 4), (8, 3), (12, 2), (24, 1)],
           [(1, 16), (2, 8), (4, 4), (8, 2), (16, 1)],
           [(1, 101), (101, 1)],
           [(1, 99), (3, 33), (9, 11), (11, 9), (33, 3), (99, 1)]]
    for i in range(len(test)):
        n = test[i]
        e = exp[i]
        f = factorize(n)
        assert f == e

def sub_parts_of_number(n, e, digits_per_piece):
    parts = []
    # ec is the e cursor
    # nc is n curso
    ec = e - digits_per_piece
    nc = n
    while ec >= 0:
        j = nc // 10 ** ec
        nc = nc - ((nc // 10**ec) * 10**ec)
        parts.append(j)
        ec = ec - digits_per_piece
    
    return parts


def test_sub_parts_of_number():
    numbers = [1, 123, 123456, 12345678, 1234567890]

    digit_counts = [[1],
                    [1],
                    [1, 2, 3],
                    [1, 2, 4],
                    [1, 2, 5]]
    
    expected_parts = [[[1]],
                      [[1, 2, 3]],
                      [[1, 2, 3, 4, 5, 6], [12, 34, 56], [123, 456]],
                      [[1, 2, 3, 4, 5, 6, 7, 8], [12, 34, 56, 78], [1234, 5678]],
                      [[1, 2, 3, 4, 5, 6, 7, 8, 9, 0], [12, 34, 56, 78, 90], [12345, 67890]]]
    
    for i in range(len(numbers)):
        n = numbers[i]
        e = number_of_digits(n)
        dig_counts = digit_counts[i]
        exp_parts = expected_parts[i]
        for j in range(len(dig_counts)):
            digits_per_piece = dig_counts[j]
            exp = exp_parts[j]
            got = sub_parts_of_number(n,e, digits_per_piece)
            assert got == exp

        

def process_part_2(ranges):
    bad_numbers = []
    for (start, stop) in ranges:
        old_e = None
        factors = None
        for n in range(start, stop+1):
            # n is the number we're dealing with

            # Get the number of digits.
            e = number_of_digits(n)
            if old_e != e:
                factors = factorize(e)

            # a number like 240240 has 6 digits,
            # so the factors are:
            # (1, 6)
            # (2, 3)
            # (3, 2)
            # (6, 1)
            #
            # For (1, 6), break the number into 6 pieces 1 digit long
            # and compare them to see if they're all the same
            # 
            # For (2, 3), break the number into 3 pieces, 2 digits long
            # and compare them to see if they're all the same

            # Ignore the last factors s
            for i in range(len(factors)-1):
                (digits_per_piece, num_pieces) = factors[i]
                
                parts = []
                # ec is the e cursor
                # nc is n curso
                ec = e - digits_per_piece
                nc = n
                while ec >= 0:
                    j = nc // 10 ** ec
                    nc = nc - ((nc // 10**ec) * 10**ec)
                    parts.append(j)
                    ec = ec - digits_per_piece
                
                # if the parts are all the same, then this is a bad number.
                if len(set(parts)) == 1:
                    bad_numbers.append(n)
                    #print(f"part 2 bad number: {n}")
                    break
    
    return sum(bad_numbers)


def test_considerable_ranges():
    ranges = [(123, 100005), 
              (12, 100005),
              (12, 98),
              (0, 98)]
    expected_considerable_ranges = [[(1000, 10000), (100000, 100006)],
                                    [(12, 100), (1000, 10000), (100000, 100006)],
                                    [(12, 99)],
                                    [(10, 99)]]
    for i in range(len(ranges)):
        r = ranges[i]
        exp = expected_considerable_ranges[i]
        got = considerable_ranges(r)
        assert got == exp

    expected_all_considerable = []
    for i in range(len(expected_considerable_ranges)):
        exp = expected_considerable_ranges[i]
        expected_all_considerable.extend(exp)

    got = gather_all_considerable_ranges(ranges)
    assert got == expected_all_considerable



test = False

if test:
    test_considerable_ranges()
    test_factorize()
    test_sub_parts_of_number()

data = input_data(test, None)

st = process_time()

ranges = parse_data(data)

result = process_part_1(ranges)

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

result_2 = process_part_2(ranges)

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







from time import process_time
st = process_time()
# Do the work
et = process_time()
total_time = et-st
print(f"Time: {total_time:.2e}")
