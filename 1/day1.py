# Advent of Code day 1




def digit_trans_map():
    trans = {}
    for i in range(0,255):
        trans_value = None
        if (i>=48 and i<=57):
            trans_value = chr(i)
        trans[i] = trans_value
    return trans

def digit_lookup_map():
    d_map = {}
    d_map[0] = ['0','zero']
    d_map[1] = ['1','one']
    d_map[2] = ['2','two']
    d_map[3] = ['3','three']
    d_map[4] = ['4','four']
    d_map[5] = ['5','five']
    d_map[6] = ['6','six']
    d_map[7] = ['7','seven']
    d_map[8] = ['8','eight']
    d_map[9] = ['9','nine']
    return d_map

def digit_to_idx_map():
    d_map = {}
    for i in range(0,10):
        d_map[i] = []
    return d_map




def extract_number_from_digits_or_string(s):
    d_lookup_map = digit_lookup_map()

    d_idx_map = digit_to_idx_map()

    # Find the indices of each representation
    for i in d_lookup_map.keys():
        lookup_values = d_lookup_map[i]
        for l in lookup_values:
            start_idx = 0
            idx = s.find(l,start_idx)
            while idx>=0:
                d_idx_map[i].append(idx)
                start_idx = idx+len(l)
                idx = s.find(l,start_idx)

    # We have identified all the indexs for each
    # number in the string.
    # Cycle through the keys and find the number with the lowest
    # and the number with the highest index.
    low_high = [None,None]
    low_n = None
    high_n = None
    for i in d_idx_map.keys():
        indexes = d_idx_map[i]
        [low, high] = low_high
        for j in indexes:
            # initialize low_high on the first go round
            if low == None:
                low = j
                low_n = i
                high = j
                high_n = i

            if j < low:
                low = j
                low_n = i
            if j > high:
                high = j
                high_n = i
        
        low_high = [low,high]
        
    n = low_n*10 + high_n
    print(f"{s.strip()} maps to {str(n)}")
    return n



def extract_just_digits(input):
    # This is part 1 of advent of code
    trans = digit_trans_map()

    numbers = []
    for aLine in input:
        s = aLine.translate(trans)
        num_str = None
        if len(s) == 0:
            num_str = 0
        elif len(s) == 1:
            num_str = s+s
        else:
            a = s[0]
            b = s[-1]
            num_str = a+b
        
        numbers.append(int(num_str))

    s = sum(numbers)

    print(s)


input_path = "./input.txt"
#input_path = "./testInput.txt"
#input_path = "./test_input_2.txt"

input = open(input_path).readlines()

numbers = []
for s in input:
    n = extract_number_from_digits_or_string(s)
    numbers.append(n)

print(sum(numbers))