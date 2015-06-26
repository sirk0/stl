class StlAsciiFormatError(Exception):
    pass

class Stl(object):
    def __init__(self, path):
        self.counter = -1
        self.data = self.read_ascii(path)

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
        return float(v1), float(v2), float(v3)

    def read_ascii(self, path):
        result = []
        with open(path) as f:
            self.read_line_equals(f, 'solid')

            while True:
                self.line = f.readline()[:-1]
                self.counter+=1
                if self.line == 'endsolid':
                    return result
                elif self.line.startswith('facet normal '):
                    n1, n2, n3 = self.line[13:].split()

                self.read_line_equals(f, 'outer loop')

                v1, v2, v3 = self.read_3_floats(f, 'vertex ', 7)
                v4, v5, v6 = self.read_3_floats(f, 'vertex ', 7)
                v7, v8, v9 = self.read_3_floats(f, 'vertex ', 7)

                self.read_line_equals(f, 'endloop')
                self.read_line_equals(f, 'endfacet')
 
                result.append([float(n1), float(n2), float(n3), v1, v2, v3, v4, v5, v6, v7, v8, v9])

        return result
