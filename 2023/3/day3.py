# Advent of Code
import os
from enum import IntEnum
import time

class PartNum:
    # Define the PartNum by its location in the data
    # where i is the row, 
    # j is the index of the first digit
    # len is the length
    #
    # So this data would generate two PartNums:
    # ...*......
    # ..35..633.
    # ......#... 
    # 
    # p1 = PartNum(1,2,2) to represent 35
    # p2 = PartNum(1,6,3) to represent 633
    def __init__(self, i:int, j:int, len:int):
        self.i = i
        self.j = j
        self.len = len
  
    # Returns a list of (i,j) tuples describing
    # the indices of the window around self.
    def window(self):
        w = []
        for i in range(self.i-1,self.i+2):
            if i == self.i:
                w.append((i,self.j-1))
                w.append((i,self.j+self.len))
            else:
                for j in range(self.j-1,self.j+self.len+1):
                    w.append((i,j))
        return w
    
    # Make sure the window function is working
    def testWindow(self):
        p1 = PartNum(1,6,3)
        w = p1.window()
        expect = [(0,5),
                  (0,6),
                  (0,7),
                  (0,8),
                  (0,9),
                  (1,5),
                  (1,9),
                  (2,5),
                  (2,6),
                  (2,7),
                  (2,8),
                  (2,9),]
        if w != expect:
            print("!!!--WINDOW TEST FAILED--!!!")
            return False
        else:
            print("WINDOW TEST PASSED")
            return True
    
    def __str__(self):
        s = f"partNum: {self.i,self.j,self.len}"
        return s
    
    def __repr__(self):
        s = f"partNum: {self.i,self.j,self.len}"
        return s

# Input data comes in looking like this:
# ...*......
# ..35..633.
# ......#... 
# 
# Pad it out with periods so that all partNum windows 
# will be valid.
# 
# Output data looks like this:
# ............
# ....*.......
# ...35..633..
# .......#....
# ............
def pad_input_data(inList:list):
    out = []
    lineLen = len(inList[0])
    out.append("."*(lineLen+2))
    for aLine in inList:
        newLine = "." + aLine + "."
        out.append(newLine)
    out.append("."*(lineLen+2))
    return out


def test_result(part:int):
    if part==1:
        return 4361
    else:
        return 467835
    
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
    input_path = os.path.curdir + os.path.sep + file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines

# Read through the data
def parse_data_for_numbers(data):
    part_nums = []
    for i in range(0,len(data)):
        aLine = data[i]
        #print(aLine)

        # Build a little state machine for this extraction.
        in_num = False
        num_start_idx = 0
        num_len = 0
        for j in range(0,len(aLine)):
            c = aLine[j]
            if c in "0123456789":
                if in_num == False:
                    in_num = True
                    num_start_idx = j
                    num_len = num_len+1
                else:
                    num_len = num_len+1
            else:
                if in_num:
                    # We have come to the end of a number
                    in_num = False
                    p = PartNum(i,num_start_idx,num_len)
                    part_nums.append(p)
                    num_start_idx = 0
                    num_len = 0

    return part_nums

# Read through the data seeking stars: "*"
# Returns a list of indices
def parse_data_for_stars(data):
    stars = []
    for i in range(0,len(data)):
        aLine = data[i]
        for j in range(0,len(aLine)):
            c = aLine[j]
            if c == "*":
                stars.append((i,j))
    return stars

def part_num_string_from_data(p:PartNum, data):
    s = data[p.i][p.j:p.j+p.len]
    return s

def part_num_int_from_data(p:PartNum, data):
    s = part_num_string_from_data(p, data)
    return int(s)

def window_string(p:PartNum, data):
    # Returns a string that is the concatenation of all
    # the characters in the partNum's window
    # 
    # So if your data looks like this:
    # ............
    # .467..114...
    # ....*....... 
    # 
    # Then the window around 467 is the chracters between ||
    # below, excluding the 467
    # |.....|.......
    # |.467.|.114...
    # |....*|....... 
    #
    # So the resulting window_string is "....." + "." + "." + "....*"
    # or, put together: "...........*"
    window = p.window()
    s = ""
    for (i,j) in window:
        s = s+data[i][j]
    return s

def window_string_contains_symbol(ws):
    # Window strings looks like this (but can be varying lengths)
    # Symbols are any character not in "0123456789."
    # ....+.......
    # .......*....
    # ...$........
    
    # This trans dict will map . and all the digits to None
    trans = {46:None}
    for i in range(48,58):
        trans[i] = None
    t = ws.translate(trans)
    return len(t)>0



def part_one(test):
    raw_data = input_data(test,1)
    data = pad_input_data(raw_data)

    #print(data)
    part_nums = parse_data_for_numbers(data)

    result = 0
    for p in part_nums:
        n = part_num_int_from_data(p,data)
        ws = window_string(p,data)
        if window_string_contains_symbol(ws):
            result = result+n
    
    return result

def product_from_list(inNumbers:list):
    result = 1
    for i in inNumbers:
        result = result*i
    return result

def part_two(test):
    raw_data = input_data(test,1)
    data = pad_input_data(raw_data)

    #for s in data:
    #    print(s)
    #print(data)
    part_nums = parse_data_for_numbers(data)
    stars = parse_data_for_stars(data)

    star_to_partnum_map = {}
    for s in stars:
        star_to_partnum_map[s] = []

    for p in part_nums:
        window = p.window()
        for s in stars:
            if s in window:
                star_to_partnum_map[s].append(p)

    result = 0
    for s in star_to_partnum_map:
        part_num_list = star_to_partnum_map[s]
        if len(part_num_list) == 2:
            gear_values = []
            for p in part_num_list:
                gear_values.append(part_num_int_from_data(p,data))
            result = result + product_from_list(gear_values)
    return result


st = time.process_time()

test = False
result = part_one(test)
#print(f"Part 1 Result: {result}")
if test:
    check_test_result(result, 1)

result = part_two(test)
#print(f"Part 2 Result: {result}")
if test:
    check_test_result(result, 2)

et = time.process_time()

# get execution time
res = et - st
print('CPU Execution time:', res, 'seconds')