class MStr:
    def __init__(self, s: str):
        self.s = s

    def __repr__(self):
        return f"{id(self)}: {self.s}"

def change_m_str(m: MStr):
    cur_s = m.s
    new_s = cur_s + " changed"
    m.s = new_s

m_str = MStr("Zack wuz here")

print(m_str)
change_m_str(m_str)
print(m_str)

def change_set(s: set):
    s |= set(["e", "f", "g"])

a_set = set(["a", "b", "c"])

print(a_set)
change_set(a_set)
print(a_set)



def change_matrix(matrix):
    s = matrix[0]
    s = s[:7] + "@" + s[8:]
    matrix[0] = s


def print_matrix(matrix):
    for row in matrix:
        print(row)

matrix = ['.......^.......',
          '......^.^......',
          '.....^.^.^.....',
          '....^.^...^....',
          '...^.^...^.^...',
          '..^...^.....^..',
          '.^.^.^.^.^...^.']

print_matrix(matrix)
change_matrix(matrix)
print_matrix(matrix)


matrix = ['.......^.......',
          '......^.^......',
          '.....^.^.^.....',
          '....^.^...^....',
          '...^.^...^.^...',
          '..^...^.....^..',
          '.^.^.^.^.^...^.']

print("=-=-=-=-=-=")

def depth_first_count_nodes(r, c, matrix):
    row = matrix[r]
    val = row[c]
    print(f"{r=}, {c=}, {val=}")
    print_matrix(matrix)
    count = 0
    if val == "^":
        count = 1
        # Mark this element as counted by changing
        # it from "^" to "@"
        new_row = row[:c] + "@" + row[c+1:]
        matrix[r] = new_row
        if len(matrix) > r+1 and c-1 >= 0:
            count += depth_first_count_nodes(r+1, c-1, matrix)
        if len(matrix) > r+1 and c+1 < len(row):
            count += depth_first_count_nodes(r+1, c+1, matrix)
    return count

count = depth_first_count_nodes(0, 7, matrix)

print("=-=-=-=-=-=")

print_matrix(matrix)

print(count)