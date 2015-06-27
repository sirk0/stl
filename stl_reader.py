class Triangle(object):
    def __init__(self, normal, point1, point2, point3):
        self.normal = normal
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

class Stl(object):
    def __init__(self, triangles):
        self.triangles = triangles

    def __len__(self):
        return len(self.triangles)

class StlAsciiFormatError(Exception):
    pass

class StlReader(object):
    def __init__(self):
        self.counter = -1
        # self.data = self.read_ascii(path).triangles

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
        return [float(p) for p in v1, v2, v3]

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
