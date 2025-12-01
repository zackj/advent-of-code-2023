# Advent of Code
import os
from enum import IntEnum

class C(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

def test_result(part:int):
    if part==1:
        return 8
    else:
        return 2286

def input_data(test_mode:bool, i:int):
    if test_mode:
        file_name = "test_input_" + str(i) + ".txt"
        file_name = "test_input.txt"
    else:
        file_name = "input_" + str(i) + ".txt"
        file_name = "input.txt"
    input_path = os.path.curdir + os.path.sep + file_name
    return open(input_path).readlines()

def initial_bag():
    bag = {C.RED:12, C.GREEN:13, C.BLUE:14}
    return bag

def empty_bag():
    bag = {C.RED:0, C.GREEN:0, C.BLUE:0}
    return bag

def color_lookup_map():
    c_map = {}
    c_map[C.RED] = 'red'
    c_map[C.GREEN] = 'green'
    c_map[C.BLUE] = 'blue'
    return c_map

def split_game(game:str):
    # game looks like any of the following:
    # '1 red, 2 green, 6 blue'
    # '3 blue, 4 red'
    # '2 green'
    # etc
    d = {C.RED:0, C.GREEN:0, C.BLUE:0}
    game_parts = game.split(", ")
    for a_part in game_parts:
        num,color = a_part.split(" ")
        key = None
        if color == "red":
            key = C.RED
        elif color == "green":
            key = C.GREEN
        else:
            key = C.BLUE
        d[key] = int(num)
    
    return d

def games_by_index(data:list):
    games_by_index = {}
    for aRow in data:
        # Each row looks like this:
        # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        num_part, games_part = aRow.strip().split("Game ")[1].split(": ")
        num = int(num_part)
        game_strings = games_part.split("; ")
        game_dicts = []
        for game in game_strings:
            d = split_game(game)
            game_dicts.append(d)
        games_by_index[num] = game_dicts
    return games_by_index


def part_one():
    # Determine which games are possible
    # and return the sum of their indices
    result = 0

    for n in games.keys():
        game_dicts = games[n]
        ok = True
        for a_game in game_dicts:
            ok = ok & (a_game[C.RED] <= bag[C.RED])
            ok = ok & (a_game[C.GREEN] <= bag[C.GREEN])
            ok = ok & (a_game[C.BLUE] <= bag[C.BLUE])
        if ok:
            #print(f"Game {n} is ok")
            result = result+n

    return result

def part_two():
    # Determine the smallest number of red, green, and blue cubes
    # that would make a game possible.
    # Then multiply those three values together
    # and sum them all up.
    result = 0

    for n in games.keys():
        # Get the minimum number of r,g,b cubes
        # required for each game to be possible.
        new_bag = empty_bag()
        game_dicts = games[n]
        for a_game in game_dicts:
            r = a_game[C.RED]
            g = a_game[C.GREEN]
            b = a_game[C.BLUE]

            if r > new_bag[C.RED]:
                new_bag[C.RED] = r
            if g > new_bag[C.GREEN]:
                new_bag[C.GREEN] = g
            if b > new_bag[C.BLUE]:
                new_bag[C.BLUE] = b
        
        # The "power" of the game is the product of
        # the minimum number of red, green, and blue cubes
        power = new_bag[C.RED]*new_bag[C.GREEN]*new_bag[C.BLUE]
        #print(f"Game {n} has power {power}")
        result = result+power

    return result

def check_test_result(result:int, part:int):
    expect = test_result(part)
    if result != expect:
        print(f"{str(part)} FAILED TEST. Got {result} expected {expect}")
    else:
        print(f"{str(part)} PASSSED TEST.")


test = False
data = input_data(test,1)
games = games_by_index(data)
bag = initial_bag()

# We now have the games parsed out.
# Time to test them.
result = part_one()
print(f"Part 1 Result: {result}")

if test:
    check_test_result(result, 1)

result = part_two()
if test:
    check_test_result(result, 2)
print(f"Part 2 Result: {result}")




