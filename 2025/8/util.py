from time import process_time
import pathlib
from datetime import datetime


# Read in the data from a text file and strip out newlines.
def input_data(test_mode: bool, i: int) -> list:
    if test_mode:
        file_name = "test_input" + ("" if i == None else str(i)) + ".txt"
    else:
        file_name = "input" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    input_lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return input_lines

def read_expected_result(i: int) -> int:
    file_name = "test_result" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return int(lines[0])

def read_expected_result_part_2(i: int) -> int:
    file_name = "test_result_part2" + ("" if i == None else str(i)) + ".txt"
    cur_path = pathlib.Path().resolve()
    input_path = cur_path / file_name
    lines = open(input_path).readlines()
    lines = [s.strip("\n\r") for s in open(input_path).readlines()]
    return int(lines[0])
