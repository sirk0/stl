class AsciiFormatError(Exception):
    pass

def read_stl_ascii(path):
    with open(path) as f:
        line = f.readline()
        if line.startswith('solid'):
            pass
        else:
            raise AsciiFormatError
    return True
