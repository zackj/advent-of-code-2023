# Advent of Code
from os import path
from enum import IntEnum
from time import process_time, perf_counter
from math import sqrt, ceil, floor
import functools

class HandType(IntEnum):
    FIVE_K = -1
    FOUR_K = -2
    FULL_H = -3
    THREE_K = -4
    TWO_PAIR = -5
    ONE_PAIR = -6
    HIGH_CARD = -7

@functools.total_ordering
class Hand:
    def __init__(self, s:str, joker_mode:bool) -> None:
        s_parts = s.split(' ')
        self.hand = s_parts[0].strip()
        self.bid = int(s_parts[1].strip())
        self.type = Hand.parse_hand_type(self.hand,joker_mode)
        self.joker_mode = joker_mode
        # Parse out the hand_type

    def parse_hand_type(in_s:str, joker_mode:bool) -> HandType:
        face_map={'A':0,'K':0,'Q':0,'J':0,'T':0,'9':0,'8':0,'7':0,'6':0,'5':0,'4':0,'3':0,'2':0}

        for i in range(len(in_s)):
            s = in_s[i]
            face_map[s] += 1
        
        # combo is shaped like:
        # (singles, two of a kinds, three of a kinds, four of a kinds, five of a kinds)
        combo = [0,0,0,0,0]
        # Check for 5 of a kind
        for key in face_map.keys():
            v = face_map[key]
            if v == 0:
                continue
            combo[v-1] = combo[v-1]+1
        
        combo_map = {(0,0,0,0,1):HandType.FIVE_K,
                     (1,0,0,1,0):HandType.FOUR_K,
                     (0,1,1,0,0):HandType.FULL_H,
                     (2,0,1,0,0):HandType.THREE_K,
                     (1,2,0,0,0):HandType.TWO_PAIR,
                     (3,1,0,0,0):HandType.ONE_PAIR,
                     (5,0,0,0,0):HandType.HIGH_CARD}
        
        cur_type = combo_map[tuple(combo)]
        joker_ct = face_map['J']

        # If we're not in joker mode or you don't have jokers anyway
        # then we're done.
        if joker_mode == False or joker_ct==0:
            return cur_type

        # The number of jokers determines the possible improvements
        # 2JJJJ has 4 jokers, so it is already 4 of a kind. It becomes 5 of a kind.

        # Handle all the possible promotions.
        # ie: A full house **### either has 0, 2, or 3 jokers
        
        # You have 1 Joker
        if joker_ct == 1:
            # Possible hands:
            # @#$%J
            # @@$%J
            # @@@%J
            # @@@@J
            # @@$$J
            promotion_map = {HandType.HIGH_CARD:HandType.ONE_PAIR,
                             HandType.ONE_PAIR:HandType.THREE_K,
                             HandType.TWO_PAIR:HandType.FULL_H,
                             HandType.THREE_K:HandType.FOUR_K, 
                             HandType.FOUR_K:HandType.FIVE_K}
            return promotion_map[cur_type]
        
        # You have 2 Jokers
        if joker_ct == 2:
            # Possible hands:
            # @#$JJ
            # @@$JJ
            # @@@JJ
            promotion_map = {HandType.ONE_PAIR:HandType.THREE_K,
                             HandType.TWO_PAIR:HandType.FOUR_K,
                             HandType.FULL_H:HandType.FIVE_K}
            return promotion_map[cur_type]

        # You have 3 Jokers
        if joker_ct == 3:
            # Possible hands:
            # @#JJJ
            # @@JJJ
            promotion_map = {HandType.THREE_K:HandType.FOUR_K,
                             HandType.FULL_H:HandType.FIVE_K}
            return promotion_map[cur_type]
        
        # You have 4 Jokers
        if joker_ct == 4:
            # Possible hands:
            # @JJJJ
            promotion_map = {HandType.FOUR_K:HandType.FIVE_K}
            return promotion_map[cur_type]
        
        if joker_ct == 5:
            return cur_type
        
        
        
        
        


    def _is_valid_operand(self,other):
        return (hasattr(other, "type") and
                hasattr(other, "bid") and
                hasattr(other, "type") and
                hasattr(other, "joker_mode"))
    
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.hand == other.hand
        
    def __lt__(self, other): 
        if not self._is_valid_operand(other):
            return NotImplemented

        val_map={'A':13,'K':12,'Q':11,'J':10,'T':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}

        if self.joker_mode:
            val_map['J']=0

        # Use score property
        if self.type != other.type:
            return self.type < other.type

        # The types were identical, so go card by card
        for i in range(len(self.hand)):
            my_i_val = val_map[self.hand[i]]
            other_i_val = val_map[other.hand[i]]
            if my_i_val == other_i_val:
                continue
            return my_i_val < other_i_val
        
        # The hands were identical.
        # The spec does not include this, but what the heck
        # Let's allow bid to be the final arbiter
        print("YOU SHOULD NOT GET HERE")
        return self.bid<other.bid

    def __str__(self) -> str:
        s = f"hand: {self.hand,self.bid,self.type}"
        return s
    
    def __repr__(self) -> str:
        return self.__str__()

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
        return 6440
    else:
        return 5905
    
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

def parse_data(data,joker_mode:bool) -> list:
    hands = []
    for i in range(len(data)):
        s = data[i]
        aHand = Hand(s,joker_mode)
        hands.append(aHand)
    return hands


def solve(hands):
    sort_hands = sorted(hands)
    result = 0
    for i in range(len(sort_hands)):
        h = sort_hands[i]
        result = result + (h.bid * (i+1))
    return result

def part_one(data):
    hands = parse_data(data,False)
    result = solve(hands)
    return result

def part_two(data):
    hands = parse_data(data,True)
    result = solve(hands)
    return result


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

