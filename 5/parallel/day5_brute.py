# Advent of Code
import os
from enum import IntEnum
import time
import sys

class Seed_With_Ranges:
    def __init__(self,in_seeds:list):
        # in_seeds is a list like:
        # [79, 14, 55, 13]
        # where each pair is a start and a length of a range
        # Parse that list into all the indices of ranges
        self.ranges = []
        self.lengths = []
        for i in range(0,len(in_seeds),2):
            start = in_seeds[i]
            length = in_seeds[i+1]
            self.ranges.append(range(start,start+length))
            self.lengths.append(length)
            

    def seed_for_idx(self, idx):
        cur_offset = 0
        for i in range(len(self.lengths)):
            length = self.lengths[i]
            cur_offset = cur_offset+length
            if idx<cur_offset:
                offset = sum(self.lengths[:i])
                r = self.ranges[i][idx-offset]
                return r


    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < sum(self.lengths):
            result = self.seed_for_idx(self.i)
            self.i += 1
            return result
        else:
            raise StopIteration
    
    def test_seed_with_ranges(self):
        s = Seed_With_Ranges([79,14,55,13])
        my_iter = iter(s)
        expect = [79,80,81,82,83,84,85,86,87,88,89,90,91,92,55,56,57,58,59,60,61,62,63,64,65,66,67]
        result = [seed for seed in my_iter]
        if result != expect:
            print(f"SEED_WITH_RANGE TEST FAILED. Got {result} expected {expect}")
            return False
        return True



class ZMap:
    # a ZMap is an object with the following attributes
    # name: "fertilizer-to-water map:"
    # srcStarts: [start integers for source]
    # dstStarts: [start integers for dest]
    # lengths: [lengths of ranges]
    # srcRanges: [range objects corresponding to srcStarts]
    #
    # All four list will be the same length

    def __init__(self, segment:list):
        # A segment is a list like:
        # ['seed-to-soil map:', '50 98 2', '52 50 5']
        # Where the first element is the identifier and the subsequent
        # elements describe the map ranges with the following indexes:
        # 0: destination start idx
        # 1: source start idx
        # 2: range length
        #
        # For example:
        # 50 98 2
        # 52 50 5
        # means:
        # 50 maps to 52
        # 51 maps to 53
        # 52 maps to 54
        # 53 maps to 55
        # 54 maps to 56
        # 98 maps to 50
        # 99 maps to 51
        self.name = segment[0]
        self.srcStarts = []
        self.dstStarts = []
        self.lengths = []
        self.srcRanges = []

        for aPart in segment[1:]:
            map_values = parse_numbers_from_spaced_string(aPart)
            [dstStart, srcStart, length] = map_values
            self.srcStarts.append(srcStart)
            self.dstStarts.append(dstStart)
            self.lengths.append(length)
        
        for i in range(len(self.srcStarts)):
            srcStart = self.srcStarts[i]
            length = self.lengths[i]
            self.srcRanges.append(range(srcStart, srcStart+length))

    def lookup_idx(self, in_:int):
        ranges = self.srcRanges
        idx = None
        for i in range(len(self.srcRanges)):
            r = self.srcRanges[i]
            if in_ in r:
                idx = i
                break
        return idx
        
    def map(self, in_:int):
        idx = self.lookup_idx(in_)
        if idx == None:
            return in_
        
        srcStart = self.srcStarts[idx]
        dstStart = self.dstStarts[idx]
        offset = in_ - srcStart
        return dstStart+offset
    
    def test_map(self):
        test_data = ["seed-to-soil map:", "50 98 2", "52 50 5"]
        zMap = ZMap(test_data)
        test_values = [50,51,52,53,54,98,99]
        expect_values = [52,53,54,55,56,50,51]
        
        result = []
        for i in range(len(test_values)):
            test = test_values[i]
            result.append(zMap.map(test))
        
        if result != expect_values:
            print(f"TEST_MAP_PARSING FAILED. Got {result} expected {expect_values}")
            return False

        return True


# A spaced string of numbers is like this: 
# 83 86  6 31 17  9 48 53 
# Parse just the numbers into a list of integers.
def parse_numbers_from_spaced_string(in_s:str):
    l = [int(s) for s in in_s.split(' ') if len(s)>0]
    return l

def test_result(part:int):
    if part==1:
        return 35
    else:
        return 46
    
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
    input_path = os.path.curdir + os.path.sep + file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines

def parse_segment_to_map(segment):
    # A segment is a list like:
    # ['fertilizer-to-water map:', '49 53 8', '0 11 42', '42 0 7', '57 7 4']
    # Where the first element is the identifier and the subsequent
    # elements describe the map with the following indexes:
    # 0: destination range start
    # 1: source rance start
    # 2: range length
    #
    # For example:
    # 50 98 2
    # means:
    # 98 maps to 50
    # 99 maps to 51
    map_desc = segment[0]
    map_dict = {}
    
    for aPart in segment[1:]:
        map_values = parse_numbers_from_spaced_string(aPart)
        [destStart, srcStart, length] = map_values
        for i in range(length):
            map_dict[srcStart+i] = destStart+i

    return {map_desc:map_dict}

def parse_seed_row(s):
    # Seed row is the first row and looks like this:
    # seeds: 79 14 55 13
    num_str = s.split('seeds:')[1]
    seeds = parse_numbers_from_spaced_string(num_str)
    return seeds

def parse_data(data):
    blank_rows = [i for i, x in enumerate(data) if len(x)==0]
    blank_rows.append(len(data))
    seeds = parse_seed_row(data[0])
    maps = []
    last_idx = 2
    for i in range(1,len(blank_rows)):
        idx = blank_rows[i]
        segment = data[last_idx:idx]
        #print(idx)
        #print(segment)
        this_map = ZMap(segment)
        maps.append(this_map)
        last_idx = idx+1

    return (seeds,maps)

def traverse_maps_for_seed(maps,seed):
    n = seed
    for i in range(len(maps)):
        zMap = maps[i]
        n = zMap.map(n)
    return n


def part_one(test:bool, input_idx:int):
    data = input_data(test,input_idx)
    
    (seeds,maps) = parse_data(data)
    lowest = None
    for i in range(len(seeds)):
        seed = seeds[i]
        n = traverse_maps_for_seed(maps, seed)
        #print(f"{i} has location number: {n}")
        if i == 0 or n<lowest:
            lowest = n
    
    return lowest


    

def part_two(test:bool, input_idx:int):
    data = input_data(test,input_idx)
    
    (raw_seeds,maps) = parse_data(data)
    seed_with_ranges = Seed_With_Ranges(raw_seeds)
    
    seed_iter = iter(seed_with_ranges)
    lowest = None
    cur = 0
    for seed in seed_iter:
        n = traverse_maps_for_seed(maps, seed)
        if cur%10000==0:
            print(f"{cur}: {seed} has location number: {n}")
        if lowest == None or n<lowest:
            lowest = n
        cur += 1
    
    return lowest



input_idx = int(sys.argv[1])


#if ZMap.test_map(1) == False:
#    quit(1)

#if Seed_With_Ranges.test_seed_with_ranges(1) == False:
#    quit(1)

st = time.process_time()

test = False
result = part_one(test, input_idx)
print(f"Part 1 Result: {result}")
if test:
    check_test_result(result, 1)

result = part_two(test, input_idx)
print(f"Part 2 Result: {result}")
if test:
    check_test_result(result, 2)

et = time.process_time()
# get execution time
res = et - st
if test == False:
    print('CPU Execution time:', res, 'seconds')