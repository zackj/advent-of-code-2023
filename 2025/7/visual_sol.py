def print_matrix(matrix):
    for row in matrix:
        print(row)


def replace_char_at_index(s: str, c: str, i: int):
    s = s[:i] + c + s[i+1:]
    return s

start_idx = 7

matrix = ['...............',
          '.......^.......',
          '...............',
          '......^.^......',
          '...............',
          '.....^.^.^.....',
          '...............',
          '....^.^...^....',
          '...............',
          '...^.^...^.^...',
          '...............',
          '..^...^.....^..',
          '...............',
          '.^.^.^.^.^...^.',
          '...............']

print_matrix(matrix)

print("=-=-=-=-=-=-=-=")

matrix[0] = replace_char_at_index(matrix[0], '|', start_idx)

print("=-=-=-=-=-=-=-=")

print_matrix(matrix)
pass



# Produce a new row by splitting or perpetuating tachyons
# RULE 1:
#   .......|.......
# + .......^.......
# = ......|.|......
#
# RULE 2:
#   .......|.......
# + ...............
# = .......|.......
#
# Return the new row and the number of splits encountered
def split_tachyons(s1, s2) -> tuple:
    split_count = 0
    r = '.' * len(s1)
    for i in range(len(s1)):
        if s1[i] != '|':
            continue # This isn't a tachyon
        if s2[i] == '^':
            split_count += 1
            if (i-1 >= 0):
                r = replace_char_at_index(r, '|', i-1)
            if (i+1 < len(r)):
                r = replace_char_at_index(r, '|', i+1)
        elif s2[i] == '.':
            r = replace_char_at_index(r, '|', i)
    return (r, split_count)
        


def process_matrix(matrix):
    split_count = 0

    for i in range(1, len(matrix), 2):
        # i is indexed to the rows with ^ characters
        this_row = matrix[i]
        last_row = matrix[i-1] # There is always a prior row
        next_row, new_splits = split_tachyons(last_row, this_row)
        matrix[i+1] = next_row
        split_count += new_splits

        print_matrix(matrix)
    
    return split_count

split_count = process_matrix(matrix)

print("=-=-=-=-=-=-=-=")

print_matrix(matrix)

print(f"{split_count=}")