class StlAsciiFormatError(Exception):
    pass

def read_stl_ascii(path):
    with open(path) as f:
        counter = 0
        line = f.readline()
        if not line.startswith('solid'):
            raise StlAsciiFormatError(counter, line)

        result = []
        while True:
            line = f.readline()[:-1]
            counter+=1
            if line == 'endsolid':
                return result
            elif line.startswith('facet normal '):
                n1, n2, n3 = line[13:].split()

            line = f.readline()[:-1]
            counter+=1
            if not line == 'outer loop':
                raise StlAsciiFormatError(counter, line)

            line = f.readline()[:-1]
            counter+=1
            if line.startswith('vertex '):
                v1, v2, v3 = line[7:].split(' ')
            else:
                raise StlAsciiFormatError(counter, line)

            line = f.readline()[:-1]
            counter+=1
            if line.startswith('vertex '):
                v4, v5, v6 = line[7:].split(' ')
            else:
                raise StlAsciiFormatError(counter, line)

            line = f.readline()[:-1]
            counter+=1
            if line.startswith('vertex '):
                v7, v8, v9 = line[7:].split(' ')
            else:
                raise StlAsciiFormatError(counter, line)

            line = f.readline()[:-1]
            counter+=1
            if not line == 'endloop':
                raise StlAsciiFormatError(counter, line)

            line = f.readline()[:-1]
            counter+=1
            if not line == 'endfacet':
                raise StlAsciiFormatError(counter, line)

            result.append([n1, n2, n3, v1, v2, v3, v4, v5, v6, v7, v8, v9])

    return result
