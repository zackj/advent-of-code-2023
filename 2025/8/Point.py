from math import sqrt

class Point:
    def __init__(self, x, y, z, id=None):
        self.x = x
        self.y = y
        self.z = z
        self.id = id
        self.circuit_pts = []

    def __repr__(self):
        return f'({self.id}: {self.x}, {self.y}, {self.z})'

    def distance_from_point(self, p):
        dx = self.x - p.x
        dy = self.y - p.y
        dz = self.z - p.z
        return sqrt(dx**2 + dy**2 + dz**2)

    def __eq__(self, p):
        return self.id == p.id and self.x == p.x and self.y == p.y and self.z == p.z
    
    def __hash__(self):
        return hash((self.id, self.x, self.y, self.z))

    def nodes_in_circuit(self, exclude=set()) -> set:
        circuit_point_ids = [p for p in self.circuit_pts if p not in exclude]
        circuit_point_ids.append(self)
        nodes = set(circuit_point_ids)
        for p in nodes.copy():
            if p not in exclude:
                new_exclude = set(list(exclude)+[self])
                nodes |= p.nodes_in_circuit(new_exclude)
        return nodes


def coord_string_to_point(s):
    x, y, z = map(int, s.split(','))
    p = Point(x, y, z)
    return p

def test_coord_string_to_point():
    p = Point(1, 2, 3, 4)
    p1 = coord_string_to_point("1,2,3")
    p1.id = 4
    assert p == p1

def test_circuits():
    p0 = Point(1, 1, 1, 0)
    p1 = Point(1, 1, 1, 1)
    p2 = Point(1, 1, 1, 2)
    p3 = Point(1, 1, 1, 3)
    p4 = Point(1, 1, 1, 4)
    p5 = Point(1, 1, 1, 5)

    a = set([p0, p1, p0])

    p0.circuit_pts.append(p1)
    p1.circuit_pts.append(p0)
    p0.circuit_pts.append(p3)
    p3.circuit_pts.append(p0)

    p0_circuits = p0.nodes_in_circuit()
    assert p0_circuits == set([p0, p1, p3])

    p3.circuit_pts.append(p4)
    p4.circuit_pts.append(p3)

    p0_circuits = p0.nodes_in_circuit()
    assert p0_circuits == set([p0, p1, p3, p4])

def test_point():
    test_coord_string_to_point()
    test_circuits()

test_point()