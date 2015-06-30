class Geometry(object):
    def __init__(self):
        self.eps = 0.00000001
        self.eps2 = self.eps**2

class Point(Geometry):
    def __init__(self, coords):
        super(Point, self).__init__()
        self.coords = coords
        self.points = [self]
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        if len(coords) != 3:
            raise TypeError
        self.bounding_box = self.get_bounding_box()

    def __len__(self):
        return len(self.coords)

    def __repr__(self):
        return 'Point ({}, {}, {})'.format(self[0], self[1], self[2])

    def __iter__(self):
        return iter(self.coords)

    def __getitem__(self, index):
        return self.coords[index]

    def __eq__(self, point2):
        return all(abs(self[i]-point2[i]) < self.eps for i in range(3))

    def get_bounding_box(self):
        return BoundingBox(self, self)

class BoundingBox(Geometry):
    def __init__(self, point_min, point_max):
        super(BoundingBox, self).__init__()
        if type(point_min) != Point:
            raise TypeError
        if type(point_max) != Point:
            raise TypeError
        self.min = point_min
        self.max = point_max
        self.points = [self.min, self.max]

    def __repr__(self):
        return 'Bounding box ({}, {}, {}), ({}, {}, {})'.format(
            self.min[0], self.min[1], self.min[2], self.max[0], self.max[1], self.max[2])

    def __getitem__(self, index):
        return self.points[index]

    def __contains__(self, point):
        return all(self.min[i] <= point[i] <= self.max[i] for i in range(3))

    def __add__(self, bounding_box):
        p_min = Point([min(self.min[i], bounding_box.min[i]) for i in range(3)])
        p_max = Point([max(self.max[i], bounding_box.max[i]) for i in range(3)])
        return BoundingBox(p_min, p_max)

class Triangle(Geometry):
    def __init__(self, normal, point1, point2, point3):
        super(Triangle, self).__init__()
        self.normal = Point(normal)
        self.point1 = Point(point1)
        self.point2 = Point(point2)
        self.point3 = Point(point3)
        self.points = [self.point1, self.point2, self.point3]
        self.bounding_box = self.get_bounding_box()

    def __repr__(self):
        return 'Triangle ' + ','.join('(' + ','.join(str(c) for c in p.coords) + ')' for p in self.points)

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def contacts(self, other_triangle):
        same_point_pairs = sum(p1 == p2 for p2 in other_triangle for p1 in self)
        return same_point_pairs >= 2

    def point_distance2(self, point2):
        result = sum((self[i]-point2[i])**2 for i in range(3))
        return result

    def get_bounding_box(self):
        return self.point1.bounding_box + self.point2.bounding_box + self.point3.bounding_box

class Stl(Geometry):
    def __init__(self, triangles):
        super(Stl, self).__init__()
        self.triangles = triangles
        inf = float('inf')
        self.default_bounding_box = BoundingBox(
            Point([inf,inf,inf]),
            Point([-inf,-inf,-inf]))
        self.bounding_box = self.get_bounding_box()

    def __len__(self):
        return len(self.triangles)

    def __iter__(self):
        return iter(self.triangles)

    def __getitem__(self, index):
        return self.triangles[index]

    def get_bounding_box(self):
        return sum((triangle.bounding_box for triangle in self), 
            self.default_bounding_box)

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        self.bounding_box += triangle.bounding_box

    def add_stl(self, other_stl):
        for triangle in other_stl:
            self.add_triangle(triangle)

    def contacts_triangle(self, other_triangle):
        if sum(other_triangle.points[i] in self.bounding_box for i in range(3)) > 1:
            return any(my_triangle.contacts(other_triangle) 
                for my_triangle in self)
        else:
            return False
    
    def contacts_stl(self, other_stl):
        return any(self.contacts_triangle(triangle) 
            for triangle in other_stl)

class StlAsciiFormatError(Exception):
    pass

class StlReader(Stl):
    def __init__(self):
        self.counter = -1

    def _read_line_equals(self, f, line):
        self.line = f.readline()[:-1]
        self.counter+=1
        if not self.line == line:
            raise StlAsciiFormatError(self.counter, self.line)

    def _read_3_floats(self, f, prefix, shift):
        self.line = f.readline()[:-1]
        self.counter+=1
        if self.line.startswith(prefix):
            v1, v2, v3 = self.line[shift:].split(' ')
        else:
            raise StlAsciiFormatError(self.counter, self.line)
        return [float(p) for p in (v1, v2, v3)]

    def read_ascii(self, path):
        triangles = []
        with open(path) as f:
            self._read_line_equals(f, 'solid')

            while True:
                self.line = f.readline()[:-1]
                self.counter+=1
                if self.line == 'endsolid':
                    stl = Stl(triangles)
                    return stl
                elif self.line.startswith('facet normal '):
                    normal = [float(p) for p in self.line[13:].split()]

                self._read_line_equals(f, 'outer loop')

                point1 = self._read_3_floats(f, 'vertex ', 7)
                point2 = self._read_3_floats(f, 'vertex ', 7)
                point3 = self._read_3_floats(f, 'vertex ', 7)

                self._read_line_equals(f, 'endloop')
                self._read_line_equals(f, 'endfacet')
                
                triangle = Triangle(normal, point1, point2, point3)
                triangles.append(triangle)

        raise StlAsciiFormatError(self.counter, self.line)
