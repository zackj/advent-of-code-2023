# Advent of Code
from os import path
from time import process_time

class Node:
    def __init__(self, id:str, l, r) -> None:
        self.id = id
        self.l = l
        self.r = r

    def is_terminal_node(self):
        return ((self == self.l) & (self == self.r))

    def _is_valid_operand(self,other):
        return (hasattr(other, "type") and
                hasattr(other, "bid") and
                hasattr(other, "type") and
                hasattr(other, "joker_mode"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.id == other.id

    def __str__(self) -> str:
        s = f"node: {self.id,self.l.id,self.r.id}"
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

def test_result(test:int):
    if test==1:
        return 2
    elif test==2:
        return 6
    elif test==3:
        return 6
    else:
        return -123
    
def check_test_result(result:int, test:int):
    expect = test_result(test)
    if result != expect:
        print(f"{str(test)} FAILED TEST. Got {result} expected {expect}")
    else:
        print(f"{str(test)} PASSSED TEST.")

# Read in the data from a text file and strip out newlines.
def input_data(test_mode:bool, i:int):
    if test_mode:
        file_name = "test_input_" + str(i) + ".txt"
    else:
        file_name = "input_" + str(i) + ".txt"
        file_name = "input.txt"
    input_path = path.curdir + path.sep + file_name
    lines = open(input_path).readlines()
    lines = [s.rstrip("\n\r") for s in lines]
    return lines

def fix_linkedList_connections(n:Node,node_lr_info:dict,all_nodes:dict):
    this_info = node_lr_info[n.id]
    if n.l == None:
        l_id = this_info[0]
        n.l = all_nodes[l_id]["node"]
        a = 1
    if n.r == None:
        r_id = this_info[0]
        n.r = all_nodes[r_id]["node"]
        a = 1
    
    all_nodes[n.id]["fixed"] = True

    nl_fixed = all_nodes[n.l.id]["fixed"]
    nr_fixed = all_nodes[n.r.id]["fixed"]

    if ((n != n.l) & (nl_fixed == False)):
        fix_linkedList_connections(n.l,node_lr_info,all_nodes)
    if ((n != n.r) & (nr_fixed == False)):
        fix_linkedList_connections(n.r,node_lr_info,all_nodes)


# Pass [] for in_id_chain and {} for all_nodes
# when calling into this.
def build_linkedList(n_id:str,node_lr_info:dict,in_id_chain:list,all_nodes:dict):
    if n_id in all_nodes:
        return all_nodes[n_id]
    
    id_chain = in_id_chain.copy()

    this_info = node_lr_info[n_id]
    l_id = this_info[0]
    r_id = this_info[1]
    
    node_l = None
    node_r = None

    id_chain.append(n_id)
    id_chain_len = len(id_chain)
    #print(f"build_linkedList: {n_id} id_chain_len: {id_chain_len}")
    # id_chain stops us from recursing infinitely
    if ((n_id != l_id) & (l_id not in id_chain)):
        if l_id in all_nodes:
            node_l = all_nodes[l_id]["node"]
        else:
            node_l = build_linkedList(l_id, node_lr_info, id_chain, all_nodes)
    if ((n_id != r_id) & (r_id not in id_chain)):
        if r_id in all_nodes:
            node_r = all_nodes[r_id]["node"]
        else:
            node_r = build_linkedList(r_id, node_lr_info, id_chain, all_nodes)

    new = Node(n_id,node_l,node_r)
    if n_id == l_id:
        new.l = new
    if n_id == r_id:
        new.r = new
    
    all_nodes[new.id] = {"node":new,"fixed":False}
    #print(f"return: {n_id}")
    return new

def parse_data(data) -> list:
    # Parses incoming data into the turn_list
    # and the tree structure
    #
    # node_lr_by_id is a temporary store
    # for holding node map information by id
    # We take a raw string like:
    # "BBB = (DDD, EEE)"  and map it as:
    # node_lr_by_id['BBB'] = ['DDD','EEE']
    #
    node_lr_by_id={} 
    turn_list = data[0]

    node_input = data[2:]
    node_ids = []
    node_map = {}

    for i in range(len(node_input)):
        raw_s = node_input[i]
        parts = raw_s.split(" = ")
        id = parts[0]
        node_ids.append(id)

        map_parts = parts[1].split(", ")
        map_l = map_parts[0].replace("(","")
        map_r = map_parts[1].replace(")","")

        node_map[id] = (map_l, map_r)
    
    root_id = node_ids[0]
    dest_id = node_ids[-1]
    return [root_id, turn_list, dest_id, node_map]

def parse_data_ll(data) -> list:
    # Parses incoming data into the turn_list
    # and the tree structure
    #
    # node_lr_by_id is a temporary store
    # for holding node map information by id
    # We take a raw string like:
    # "BBB = (DDD, EEE)"  and map it as:
    # node_lr_by_id['BBB'] = ['DDD','EEE']
    #
    node_lr_by_id={} 
    turn_list = data[0]
    root_id = None
    node_input = data[2:]
    node_ids = []
    for i in range(len(node_input)):
        raw_s = node_input[i]
        parts = raw_s.split(" = ")
        id = parts[0]
        node_ids.append(id)
        if root_id == None:
            root_id = id
        map_parts = parts[1].split(", ")
        map_l = map_parts[0].replace("(","")
        map_r = map_parts[1].replace(")","")
        node_lr_by_id[id] = (map_l, map_r)
        if id == map_l and id == map_r:
            print(f"Terminal node row {i+2}: {id}")
    
    all_nodes = {}
    id_chain = []
    for n_id in node_ids:
        build_linkedList(n_id, node_lr_by_id, id_chain, all_nodes)
    
    for n_id in node_ids:
        root_node = all_nodes[n_id]["node"]
        fix_linkedList_connections(root_node, node_lr_by_id, all_nodes)

    # Check to make sure all nodes are mapped and
    for n_id in node_ids:
        fixed = all_nodes[n_id]["fixed"]
        if (fixed == False):
            print("NOT FIXED!")

    root_node = all_nodes["AAA"]["node"]
    dest_id = node_ids[-1]
    return [root_node, turn_list, dest_id]

def solve(root_id, turn_list, dest_id, node_map):
    cur_node_id = root_id
    step_count = 0
    reached_dest = False
    while reached_dest == False:
        if step_count%10000 == 0:
            print(f"step_count: {step_count}")
        for i in range(len(turn_list)):
            step_count += 1
            dir = turn_list[i]
            if dir == "L":
                cur_node_id = node_map[cur_node_id][0]
            else:
                cur_node_id = node_map[cur_node_id][1]
            if cur_node_id == dest_id:
                reached_dest = True
                break
    return step_count

def solve_ll(root_node, turn_list, dest_id):
    cur_node = root_node
    step_count = 0
    reached_dest = False
    while reached_dest == False:
        if step_count%10000 == 0:
            print(f"step_count: {step_count}")
        for i in range(len(turn_list)):
            step_count += 1
            dir = turn_list[i]
            if dir == "L":
                cur_node = cur_node.l
            else:
                cur_node = cur_node.r
            if cur_node.id == dest_id:
                reached_dest = True
                break
    return step_count

def part_one(data):
    #[root_node, turn_list, dest_id] = parse_data_ll(data)
    #result_ll = solve_ll(root_node, turn_list, dest_id)

    [root_node, turn_list, dest_id, node_map] = parse_data(data)
    result = solve('AAA', turn_list, 'ZZZ', node_map)

    a = 1
    return result

def solve_part_two(turn_list, node_map):
    cur_nodes = []
    for id in node_map.keys():
        if id[-1]=="A":
            cur_nodes.append(id)
    
    all_Zs = ["Z" for s in cur_nodes]
    print(cur_nodes)
    step_count = 0
    reached_dest = False
    while reached_dest == False:
        for i in range(len(turn_list)):
            step_count += 1
            dir = turn_list[i]
            new_nodes = cur_nodes.copy()
            for j in range(len(cur_nodes)):
                if dir == "L":
                    new_nodes[j] = node_map[cur_nodes[j]][0]
                else:
                    new_nodes[j] = node_map[cur_nodes[j]][1]
            #print(new_nodes)
            cur_nodes = new_nodes
            last_letters = [s[-1] for s in cur_nodes]
            if step_count>0 and step_count%10000 == 0:
                print(f"step_count: {step_count}")
                print(cur_nodes)
                print(last_letters)
            reached_dest = (last_letters == all_Zs)
            if reached_dest:
                print(cur_nodes)
                print(last_letters)
                break
    return step_count

def part_two(data):
    [root_node, turn_list, dest_id, node_map] = parse_data(data)
    result = solve_part_two(turn_list, node_map)
    return result


def test_part_one():
    test = True
    data = input_data(test,1)
    result = part_one(data)
    print(f"Part 1 Result 1: {result}")
    check_test_result(result, 1)

    data = input_data(test,2)
    result = part_one(data)
    print(f"Part 1 Result 2: {result}")
    check_test_result(result, 2)

def test_part_two():
    test = True
    data = input_data(test,3)
    result = part_two(data)
    print(f"Part 2 Result 1: {result}")
    check_test_result(result, 3)

test = False

if test:
    test_part_one()
    test_part_two()
    quit()

data = input_data(test,1)

st = process_time()

result = part_one(data)
print(f"Part 1 Result: {result}")

et = process_time()
t = et-st
print(f"Part 1 time: {t:.2e}")

quit()
st = process_time()

result = part_two(data)
print(f"Part 2 Result: {result}")

et = process_time()
t = et-st
print(f"Part 2 time: {t:.2e}")

