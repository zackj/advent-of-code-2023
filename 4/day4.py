# Advent of Code
import os
from enum import IntEnum
import time

# A card string of numbers is space separated 
# like this: 
# 83 86  6 31 17  9 48 53 
# Parse just the numbers into a list of integers.
def parse_numbers_from_card_string(in_s:str):
    l = [int(s) for s in in_s.split(' ') if len(s)>0]
    return l

class Card:
    # Define a Card
    # A card has:
    # i:int   its index
    # w:list  winning numbers
    # n:list  actual numbers
    #
    # A card looks like this:
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    # 
    # The index is 1
    # The winning numbers are 41 48 83 86 17
    # The actual numbers 83 86  6 31 17  9 48 53
    #
    # initialize a Card with the raw card string
    def __init__(self, s:str):
        c_word = "Card "
        c_idx = s.find(":")
        p_idx = s.find("|")
        idx_s = s[len(c_word):c_idx]
        w_s = s[c_idx+1:p_idx]
        a_s = s[p_idx+1:]
        
        self.i = int(idx_s)
        self.winning_numbers = parse_numbers_from_card_string(w_s)
        self.actual_numbers = parse_numbers_from_card_string(a_s)
  
    # Returns a list of actual_numbers that have a mate in 
    # winning_numbers
    # the indices of the window around self.
    def matches(self):
        l = [s for s in self.actual_numbers if s in self.winning_numbers]
        return l
    
    # You get 1 point for the first match,
    # Then that doubles for every subsequent match
    def score(self):
        score = 0
        if len(self.matches())>0:
            score = 2**(len(self.matches())-1)
        return score

    # Make sure the card's basic functionality works
    def test_card(self):
        s = "Card 1366: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        c = Card(s)

        expect_i = 1366
        expect_w = [41, 48, 83, 86, 17]
        expect_a = [83, 86, 6, 31, 17, 9, 48, 53]
        expect_m = [83, 86, 17, 48]
        expect_s = 8

        actual_matches = c.matches()
        actual_score = c.score()
        if c.i != expect_i:
            print("!!!--CARD INDEX TEST FAILED--!!!")
            print(f"Found: {c.i} expected {expect_i}")
            return False
        if c.winning_numbers != expect_w:
            print("!!!--CARD WINNING NUMBERS TEST FAILED--!!!")
            print(f"Found: {c.winning_numbers} expected {expect_w}")
            return False
        if c.actual_numbers != expect_a:
            print("!!!--CARD ACTUAL NUMBERS TEST FAILED--!!!")
            print(f"Found: {c.actual_numbers} expected {expect_a}")
            return False
        if actual_matches != expect_m:
            print("!!!--CARD MATCH TEST FAILED--!!!")
            print(f"Found: {actual_matches} expected {expect_m}")
            return False
        if actual_score != expect_s:
            print("!!!--CARD PART ONE SCORE TEST FAILED--!!!")
            print(f"Found: {actual_score} expected {expect_s}")
            return False
        print("CARD TEST PASSED")
        return True
    
    def __str__(self):
        s = f"card: {self.i,self.w,self.a}"
        return s
    
    def __repr__(self):
        s = f"card: {self.i,self.w,self.a}"
        return s

def gather_stack(cards):
    # count_map keeps track of how many of each card
    # You've won.
    # Initialize it to have 1 card for every index
    count_map = {}
    for i in range(len(cards)):
        count_map[i] = 1
    
    for i in range(len(cards)):
        c = cards[i]
        match_ct = len(c.matches())
        cur_ct = count_map[i]
        for j in range(0,cur_ct):
            for k in range(1,1+match_ct):
                count_map[i+k] = count_map[i+k]+1
    
    return count_map
    


def test_result(part:int):
    if part==1:
        return 13
    else:
        return 30
    
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

def parse_data_for_cards(data):
    cards = [Card(s) for s in data]
    return cards

def part_one(test):
    data = input_data(test,1)
    #print(data)
    cards = parse_data_for_cards(data)
    scores = [c.score() for c in cards]
    result = sum(scores)
    return result

def part_two(test):
    data = input_data(test,1)
    #print(data)
    cards = parse_data_for_cards(data)
    count_map = gather_stack(cards)
    counts = []
    for i in count_map:
        counts.append(count_map[i])
    result = sum(counts)
    return result


st = time.process_time()

Card.test_card(1)

test = False
result = part_one(test)
print(f"Part 1 Result: {result}")
if test:
    check_test_result(result, 1)

result = part_two(test)
print(f"Part 2 Result: {result}")
if test:
    check_test_result(result, 2)


et = time.process_time()
# get execution time
res = et - st
if test == False:
    print('CPU Execution time:', res, 'seconds')