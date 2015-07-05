import math
import argparse

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

    def __sub__(self, point2):
        return Point([self[i] - point2[i] for i in range(3)])

    def get_bounding_box(self):
        return BoundingBox(self, self)

    def multiply_vect(self, point2):
        v3 = [self[1]*point2[2]-point2[1]*self[2],
              -self[0]*point2[2]+point2[2]*self[0],
              self[0]*point2[1]-point2[0]*self[1]]
        return Point(v3)

    def get_vector_length(self):
        return math.sqrt(sum(self[i]**2 for i in range(3)))

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
    def __init__(self, point1, point2, point3, normal=None):
        super(Triangle, self).__init__()
        if normal is None:
            self.normal = (point3 - point1).multiply_vect(point2 - point1)
        else:
            self.normal = Point(normal)
        self.point1 = Point(point1)
        self.point2 = Point(point2)
        self.point3 = Point(point3)
        self.points = [self.point1, self.point2, self.point3]
        self.bounding_box = self.get_bounding_box()

    def __repr__(self):
        return 'Triangle ' + ','.join('(' + ','.join(str(c) for c in p.coords) + ')'
            for p in self.points)

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def contacts(self, other_triangle):
        return any(p1 == p2 for p2 in other_triangle for p1 in self)

    def get_bounding_box(self):
        return self.point1.bounding_box + self.point2.bounding_box + self.point3.bounding_box

    def get_area(self):
        v1 = self.point2 - self.point1
        v2 = self.point3 - self.point1
        v3 = v1.multiply_vect(v2)
        return v3.get_vector_length()/2.0

class Stl(Geometry):
    def __init__(self, triangles):
        super(Stl, self).__init__()
        self.triangles = triangles
        inf = float('inf')
        self.default_bounding_box = BoundingBox(
            Point([inf, inf, inf]),
            Point([-inf, -inf, -inf]))
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
        if any(other_triangle.points[i] in self.bounding_box for i in range(3)):
            return any(my_triangle.contacts(other_triangle)
                for my_triangle in self)
        else:
            return False

    def contacts_stl(self, other_stl):
        return any(self.contacts_triangle(triangle)
            for triangle in other_stl)

    def get_area(self):
        return sum(triangle.get_area() for triangle in self)

class StlAsciiFormatError(Exception):
    pass

class StlReader(object):
    def __init__(self):
        self.counter = -1
        self.line = ''

    def _read_line_equals(self, f, line):
        self.line = f.readline()[:-1]
        self.counter += 1
        if not self.line == line:
            raise StlAsciiFormatError(self.counter, self.line)

    def _read_3_floats(self, f, prefix, shift):
        self.line = f.readline()[:-1]
        self.counter += 1
        if self.line.startswith(prefix):
            try:
                v1, v2, v3 = [float(p) for p in self.line[shift:].split(' ')]
            except ValueError:
                raise StlAsciiFormatError(self.counter, self.line)
        else:
            raise StlAsciiFormatError(self.counter, self.line)
        return [v1, v2, v3]

    def read_ascii(self, path):
        triangles = []
        with open(path) as f:
            self._read_line_equals(f, 'solid')

            while True:
                self.line = f.readline()[:-1]
                self.counter += 1
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

                triangle = Triangle(point1, point2, point3, normal)
                triangles.append(triangle)

        raise StlAsciiFormatError(self.counter, self.line)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Read STL from file and calculate number of triangles')
    parser.add_argument('-i', '--input', required=True,
        help='input STL file path')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    reader = StlReader()
    stl = reader.read_ascii(args.input)
    print(len(stl))

if __name__ == '__main__':
    main()
