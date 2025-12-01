# Advent of Code
from os import path
from enum import IntEnum
from time import process_time, perf_counter
from math import sqrt, ceil, floor

# A spaced string of numbers is like this: 
# 83 86  6 31 17  9 48 53 
# Parse just the numbers into a list of integers.
def parse_numbers_from_spaced_string(in_s:str):
    l = [int(s) for s in in_s.split(' ') if len(s)>0]
    return l

def product_of_list(in_l:list):
    p = 1
    for i in in_l:
        p = p*i
    return p

def test_result(part:int):
    if part==1:
        return 288
    else:
        return 71503
    
def check_test_result(result:int, part:int):
    expect = test_result(part)
    if result != expect:
        print(f"{str(part)} FAILED TEST. Got {result} expected {expect}")
    else:
        print(f"{str(part)} PASSSED TEST.")

# Read in the data from a text file and strip out newlines.
def input_data(test_mode:bool, i:int):
    if test_mode:
        file_name = "test_input_" + str(i) + ".txt"
        file_name = "test_input.txt"
    else:
        file_name = "input_" + str(i) + ".txt"
        file_name = "input.txt"
    input_path = path.curdir + path.sep + file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines

def parse_data(data):
    times = parse_numbers_from_spaced_string(data[0].split(":")[1])
    distances = parse_numbers_from_spaced_string(data[1].split(":")[1])
    return (times, distances)

def parse_data_part_two(data):
    time_str = data[0].split(":")[1].replace(" ","")
    dist_str = data[1].split(":")[1].replace(" ","")
    times = parse_numbers_from_spaced_string(time_str)
    distances = parse_numbers_from_spaced_string(dist_str)
    return (times, distances)

# Consider a "race" to have the following components:
# x: number of seconds the button was pushed
# t: length of race
# d: distance traveled
# 
# Your speed is the number of milliseconds you hold down the button
# So if you hold the button for 5, your speed is 5
# Then the distance you travel is the remaining
# time in the race times your speed:
# d = (t-x)x
# 
# Hence, solving x^2 - tx + d = 0 
# for x gives us the number of seconds
# that achieved the current record
# 
def current_x(t,d):
    # Input the race time limit t and 
    # the race distance record d
    # and return x
    det = (t**2)-(4*d)
    det_sqrt = sqrt(det)
    x1 = (t+det_sqrt)/2
    x2 = (t-det_sqrt)/2

    # Sanity test. These should be real close to zero
    check_d1 = (x1**2)-(t*x1)+d
    check_d2 = (x2**2)-(t*x2)+d

    debug = False
    if debug:
        print(f"{t},{d}");
        print(f"{x1},{x2}")
        print(f"{check_d1},{check_d2}")

    return (x1, x2)

def winning_strategy_count(t,d):
    [x1,x2] = sorted(list(current_x(t,d)))
    [low,high] = [ceil(x1), ceil(x2)]
    addend = 0
    if low == x1:
        low = low+1
    if high == x2:
        high = high-1
        addend = 1
    count = (high-low+addend)
    debug = False
    if debug:
        print(f"low: {low}")
        print(f"high: {high}")
        print(f"t:{t}")
        print(f"d:{d}")
        for x in range(low,high+addend):
            new_d = (t-x)*x
            print(f"{x} new d:{new_d}")
    return count

def solve(times,distances):
    strategy_counts = []
    for i in range(len(times)):
        t = times[i]
        d = distances[i]
        this_count = winning_strategy_count(t,d)
        strategy_counts.append(this_count)
    result = product_of_list(strategy_counts)
    return result

def part_one(data):
    (times,distances) = parse_data(data)
    return solve(times,distances)

def part_two(data):
    (times,distances) = parse_data_part_two(data)
    return solve(times,distances)


test = False
data = input_data(test,1)

st = process_time()


result = part_one(data)
print(f"Part 1 Result: {result}")
if test:
    check_test_result(result, 1)


et = process_time()
t = et-st
print(f"Part 1 time: {t:.2e}")


st = process_time()


result = part_two(data)
print(f"Part 2 Result: {result}")
if test:
    check_test_result(result, 2)

et = process_time()
t = et-st
print(f"Part 2 time: {t:.2e}")

