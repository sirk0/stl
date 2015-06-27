class Geometry(object):
    def __init__(self):
        self.eps = 0.00000001
        self.eps2 = self.eps**2

    def point_distance2(self, p1, p2):
        result = sum((p1[i]-p2[i])**2 for i in range(3))
        return result

class Triangle(Geometry):
    def __init__(self, normal, point1, point2, point3):
        super(Triangle, self).__init__()
        self.normal = normal
        self.points = [point1, point2, point3]

    def contacts(self, other_triangle):
        same_point_pairs = sum(self.point_distance2(p1, p2) < self.eps2
            for p2 in other_triangle.points for p1 in self.points)
        return same_point_pairs >= 2

class Stl(Geometry):
    def __init__(self, triangles):
        super(Stl, self).__init__()
        self.triangles = triangles

    def __len__(self):
        return len(self.triangles)

    def contacts_triangle(self, other_triangle):
        return any(my_triangle.contacts(other_triangle) 
            for my_triangle in self.triangles)
    
    def contacts_stl(self, other_stl):
        return any(self.contacts_triangle(triangle) 
            for triangle in other_stl.triangles)

class StlAsciiFormatError(Exception):
    pass

class StlReader(object):
    def __init__(self):
        self.counter = -1

    def read_line_equals(self, f, line):
        self.line = f.readline()[:-1]
        self.counter+=1
        if not self.line == line:
            raise StlAsciiFormatError(self.counter, self.line)

    def read_3_floats(self, f, prefix, shift):
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
            self.read_line_equals(f, 'solid')

            while True:
                self.line = f.readline()[:-1]
                self.counter+=1
                if self.line == 'endsolid':
                    stl = Stl(triangles)
                    return stl
                elif self.line.startswith('facet normal '):
                    normal = [float(p) for p in self.line[13:].split()]

                self.read_line_equals(f, 'outer loop')

                point1 = self.read_3_floats(f, 'vertex ', 7)
                point2 = self.read_3_floats(f, 'vertex ', 7)
                point3 = self.read_3_floats(f, 'vertex ', 7)

                self.read_line_equals(f, 'endloop')
                self.read_line_equals(f, 'endfacet')
                
                triangle = Triangle(normal, point1, point2, point3)
                triangles.append(triangle)

        raise StlAsciiFormatError(self.counter, self.line)
